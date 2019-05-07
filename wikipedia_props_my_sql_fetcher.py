import mysql.connector
from wikipedia_props_fetcher import WikipediaPropsFetcher


class WikipediaPropsMySQLFetcher(WikipediaPropsFetcher):
    def __init__(self, user, password, host, database, query):
        """

        :param user:
        :param password:
        :param host:
        :param database:
        :param query: Sql query of form wikidata_id, wikipedia_page_id, title
        """
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
        cursor = cnx.cursor()
        cursor.execute(query)
        self.dictionary = {wikidata_id: [wikipedia_page_id, self.clean_title(title)] for
                           wikidata_id, wikipedia_page_id, title in cursor}
        cursor.close()
        cnx.close

    @staticmethod
    def clean_title(title):
        # remove all tags ''
        chars = []

        ignore_char = False
        for c in title:
            if c == '<':
                ignore_char = True
            elif c == '>':
                ignore_char = False
            else:
                if not ignore_char:
                    chars.append(c)

        cleaned_title = ''.join(chars).replace(' ', '_').replace('&amp;', '&').replace('&#39;', "'")
        return cleaned_title

if __name__ == '__main__':
    print(WikipediaPropsMySQLFetcher("root", "toor", "127.0.0.1", "mpss2019",
                                     "select cast(p1.pp_value as char(32)) as wikidata_id, p1.pp_page as " +
                                     "wikipedia_page_id, cast(p2.pp_value as char(255)) as title " +
                                     "from page_props p1, page_props p2 " +
                                     "where " +
                                     "p1.pp_propname in ('wikibase_item') and " +
                                     "p2.pp_propname in ('displaytitle') and " +
                                     "p1.pp_page = p2.pp_page " +
                                     "LIMIT 10;"))
