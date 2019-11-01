# -*- coding: utf-8 -*-
"""
<A Dynamic Graphical User Interface package, which gives users a method to construct temporary, permanent and/or a set of GUI:s for users in a simple and fast manner combined with diagnostics tools (with advance 1D and 2D plotting methods).>
    Copyright (C) <2019>  <Benjamin Edward Bolling>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import fnmatch, pytz

class CassImp:
    def __init__(self):
        
        self.datatimestamps = 0
        self.readvals = 0
        
    def attr_wildcard(self,wildcard):
        query = "SELECT cs_name, domain, family, member, name FROM att_names"
        attrs = []
        """
        hdb_cluster_old = ['b-v-db-cn-0',
                       'b-v-db-cn-1',
                       'b-v-db-cn-2',
                       'b-v-db-cn-3',
                       'b-v-db-cn-4',
                       'b-v-db-cn-5']
        """
        hdb_cluster = ['b-picard13-cas-0',
                       'b-kirk13-cas-3',
                       'b-kirk13-cas-4',
                       'b-kirk13-cas-5']
        cluster = Cluster(hdb_cluster)
        session = cluster.connect("hdb")
        
        for row in self.execute_cql_querry(session, query):
            if "g-v-csdb-0" in row.cs_name:
                attr = "/".join((row.domain, row.family, row.member, row.name))
                attrs.append(attr)
        matches = [att for att in attrs if fnmatch.fnmatch(att, wildcard)]
        return matches
        
    def execute_cql_querry(self, session, cql_querry):
        prepared_request = session.prepare(cql_querry)
        gen = session.execute(prepared_request)
        cql_rows = [row for row in gen]
        return cql_rows
        
    def get_att_data_type(self, att_conf_id, session):
        """ Return HDB++ data_type from an att_conf_id """
        cql_querry = "SELECT data_type FROM att_conf WHERE att_conf_id = {}"
        cql_querry += " ALLOW FILTERING"
        cql_querry = cql_querry.format(att_conf_id)
        reply = self.execute_cql_querry(session, cql_querry)
        data_type = reply[0].data_type
        return data_type
        
    def get_att_conf_id(self, attr_name, session):
        """ Return the HDB++ att_conf_id for one attribute """
        cql_querry = "SELECT att_conf_id FROM att_conf WHERE att_name= '{}'"
        cql_querry += " ALLOW FILTERING"
        cql_querry = cql_querry.format(attr_name)
        reply = self.execute_cql_querry(session, cql_querry)
        if not reply:
            msg = "Attribute {}: Not configured in HDB++".format(attr_name)
            raise NameError(msg)
        if len(reply) > 1:
            msg = "Attribute {}: More than one entry found in HDB++"
            raise NameError(msg)
        att_conf_id = reply[0].att_conf_id
        return att_conf_id
        
    def get_data(self, data_type, att_id, period):
            query = "SELECT * from att_{} WHERE att_conf_id = {} and period = '{}'"
            select_period = query.format(data_type, att_id, period)
            hdb_cluster = ['b-picard13-cas-0',
                       'b-kirk13-cas-3',
                       'b-kirk13-cas-4',
                       'b-kirk13-cas-5']
            cluster = Cluster(hdb_cluster)
            session = cluster.connect("hdb")
            data = self.execute_cql_querry(session, select_period)
            return data
    
    def readingdata(self,inp1,inp2,inp3):
        attr_name = inp1
        period_start =  datetime.strptime(inp2, "%Y-%m-%d")
        if inp3 == 'now':
            period_end = datetime.now()
        else:
            period_end =  datetime.strptime(inp3, "%Y-%m-%d")
        
        periods = [(period_start + timedelta(days=d)).strftime("%Y-%m-%d")
                   for d in range((period_end - period_start).days + 1)]
        all_atts = attr_name.split(";")
        for n in range(0,len(all_atts)):
            attr_name = str(all_atts[n])
            attributes = self.attr_wildcard(attr_name)
            for i, attr_name in enumerate(attributes):
                data = []
                hdb_cluster = ['b-picard13-cas-0',
                       'b-kirk13-cas-3',
                       'b-kirk13-cas-4',
                       'b-kirk13-cas-5']
                stockholm = pytz.timezone("Europe/Stockholm")
                utc = pytz.utc
                cluster = Cluster(hdb_cluster)
                session = cluster.connect("hdb")
                att_conf_id = self.get_att_conf_id(attr_name, session)
                data_type = self.get_att_data_type(att_conf_id, session)
                for period in periods:
                    data += self.get_data(data_type, att_conf_id, period)
        datatimestamps = []
        readvals = []
        for d in data:
            data_time = utc.localize(d.data_time)
            data_time = data_time.astimezone(stockholm)
            data_time = data_time.strftime('%Y-%m-%d_%H:%M:%S')
            data_time = data_time + "." + str(d.data_time_us)
            value_r = str(d.value_r)
            readvals.append(value_r)
            datatimestamps.append(data_time)
        return(datatimestamps,readvals)