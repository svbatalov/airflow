# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class SnowflakeOperator(BaseOperator):
    """
    Executes sql code in a Snowflake database

    :param snowflake_conn_id: reference to specific snowflake connection id
    :type snowflake_conn_id: string
    :param sql: the sql code to be executed
    :type sql: Can receive a str representing a sql statement,
        a list of str (sql statements), or reference to a template file.
        Template reference are recognized by str ending in '.sql'
    :param warehouse: name of warehouse which overwrite defined
        one in connection
    :type warehouse: string
    :param database: name of database which overwrite defined one in connection
    :type database: string
    """

    template_fields = ('sql',)
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self, sql, snowflake_conn_id='snowflake_default', parameters=None,
            autocommit=True, warehouse=None, database=None, *args, **kwargs):
        super(SnowflakeOperator, self).__init__(*args, **kwargs)
        self.snowflake_conn_id = snowflake_conn_id
        self.sql = sql
        self.autocommit = autocommit
        self.parameters = parameters
        self.warehouse = warehouse
        self.database = database

    def get_hook(self):
        return SnowflakeHook(snowflake_conn_id=self.snowflake_conn_id,
                             warehouse=self.warehouse, database=self.database)

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = self.get_hook()
        hook.run(
            self.sql,
            autocommit=self.autocommit,
            parameters=self.parameters)
