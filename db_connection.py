'''
Connects to the Postgres DB and performs analysis/plots on graph

Download Secure Pipes

new local forward
server address: shell.cec.wustl.edu, port: 22
ssh username, ssh password
bind address *, port 80 (or w.e is open/set below)
host address 128.252.167.175 port 5432



'''
import psycopg2 as pgres
import pandas as pd
import yaml
import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.feature_selection import RFE
from sklearn.svm import SVR


class RunAnalysis:

    # constructor, set configs from yml file
    def __init__(self, configs):
        self.configs = configs

    def open_db_connection(self):
        # create database connection
        conn = pgres.connect(database=self.configs['database'], \
                             user=self.configs['user'],
                            password=self.configs['password'], \
                             host=self.configs['host'], \
                             port=self.configs['forward_port'])
        cur = conn.cursor()
        return cur

    def attack_type(self, cur):
        # attack type vs freedom / trust
        sql = "select * from attack_targets_happiness " \
              "where targtype1 = 'Government (Diplomatic)'"
        cur.execute(sql)
        attack_targ_happiness = pd.DataFrame(cur.fetchall(),
                                             columns=['Country', 'Targ Type', 'Attacks', 'Trust', 'Freedom'])
        print attack_targ_happiness[['Attacks','Trust', 'Freedom']].corr('pearson')

    def happiness_vs_attacks(self, cur):

        # happiness vs number of terrorist attacks
        sql = "select attacks, hrank from cummulative_happiness"
        cur.execute(sql)
        cumm_happiness = pd.DataFrame(cur.fetchall(), columns = ['Attacks', 'Hrank'])
        print cumm_happiness
        print cumm_happiness.corr('pearson')

    def economy_vs_happiness(self,cur):
        sql = "select hrank, economy from happiness;"
        cur.execute(sql)
        econ_happ = pd.DataFrame(cur.fetchall(), columns=['Hrank', 'Economy'])
        print econ_happ.corr('pearson')

    def plot_attack_feature_correlations(self,cur):
        sql = "SELECT c.attacks, h.hrank, h.economy, h.family, h.health, h.freedom, h.trust, h.generosity, h.dys_residual FROM happiness as h " \
              "INNER JOIN cummulative AS c ON h.country = c.country;"

        cur.execute(sql)
        happiness_colnames = [desc[0] for desc in cur.description]
        happiness = pd.DataFrame(cur.fetchall(), columns=happiness_colnames)
        attacks = happiness.ix[:,1] # 0 for attacks, 1 for hrank
        feats = happiness.ix[:, 2:]

        x = []
        y = []
        for col in feats:
            pear_co = pd.DataFrame({'attacks':attacks, col: feats[col]}).corr('pearson')
            x.append(pear_co.columns[1])
            y.append(pear_co['attacks'][1])

        d = [l[0] for l in sorted(zip(x,y), key=lambda j:abs(j[1]),reverse=True)]

        # plot using plotly, uncomment to plot
        # data = [go.Bar(
        #     x=x,
        #     y=y
        # )]
        # layout = go.Layout(
        #     title='Correlation to Happiness Rank vs Happiness Features',
        #     xaxis=dict(
        #         title='Features',
        #         titlefont=dict(
        #             family='Courier New, monospace',
        #             size=18,
        #             color='#7f7f7f'
        #         )
        #     ),
        #     yaxis=dict(
        #         title='Correlation to Happiness Rank',
        #         titlefont=dict(
        #             family='Courier New, monospace',
        #             size=18,
        #             color='#7f7f7f'
        #         )
        #     )
        # )
        #
        # fig = go.Figure(data=data, layout=layout)
        # py.sign_in('Mranftle', 'MikQahEQpuPow1Dd5XxZ')
        # py.iplot(fig, filename='happiness_features')

    def feature_selection(self, cur):
        # rank features of happiness compared to happiness rank and number of terrorist attacks
        sql = "SELECT c.attacks, h.hrank, h.economy, h.family, h.health, h.freedom, h.trust, h.generosity, h.dys_residual FROM happiness as h " \
              "INNER JOIN cummulative AS c ON h.country = c.country;"
        cur.execute(sql)
        happiness_colnames = [desc[0] for desc in cur.description]
        happiness = pd.DataFrame(cur.fetchall(), columns=happiness_colnames)
        X = happiness.ix[:, 2:]
        estimator = SVR(kernel="linear")

        # vs hrank
        y = happiness['hrank']
        selector = RFE(estimator, n_features_to_select=1, step=1)
        selector = selector.fit(X, y)
        happ_feat_ranks = sorted(zip(selector.ranking_, happiness_colnames[2:]))

        # vs attacks
        y = happiness['attacks']
        selector = RFE(estimator, n_features_to_select=1, step=1)
        selector = selector.fit(X, y)
        attack_feat_ranks = sorted(zip(selector.ranking_, happiness_colnames[2:]))

        print 'features most correlated with number of terrorist attacks:\n', attack_feat_ranks

        print 'features most correlated with happiness ranking:\n', happ_feat_ranks

    def run(self):
        cur = self.open_db_connection()
        self.attack_type(cur)
        self.happiness_vs_attacks(cur)
        self.feature_selection(cur)
        self.economy_vs_happiness(cur)
        self.plot_attack_feature_correlations(cur)

def get_configs():
    """parse db configs from yaml
    """
    with open('configs.yml', 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as err:
            print(err)

def main():
    ra = RunAnalysis(get_configs())
    ra.run()

if __name__ == '__main__':
    main()


