from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id="",
                 table="",
                 select_sql="",
                 append_data=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql
        self.append_data = append_data

    def execute(self, context):
        self.log.info('LoadDimensionOperator has implemented')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Loading data into dimension table in Redshift")

        if self.append_data == True:
            sql_statement = 'INSERT INTO %s %s' % (self.table, self.select_sql)
            redshift_hook.run(sql_statement)
        else:
            sql_statement = 'DELETE FROM %s' % self.table
            redshift_hook.run(sql_statement)

            sql_statement = 'INSERT INTO %s %s' % (self.table, self.select_sql)
            redshift_hook.run(sql_statement)

