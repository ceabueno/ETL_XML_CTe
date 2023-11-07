from xml.dom import minidom
import os
import pandas as pd 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import pyodbc

class FileHandler(FileSystemEventHandler):
    def __init__(self, origem):
        self.origem = origem
    
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            arquivo_origem = event.src_path
            if os.path.exists(arquivo_origem):
                lista = self.extrair_informacoes_xml(arquivo_origem)
                self.criardf(lista)

    def extrair_informacoes_xml(self, arquivo_origem):
        lista = []
    
        with open(arquivo_origem, encoding='utf-8') as xml:
            try:
                Cte = minidom.parse(xml)
            except:
                doc = xml.read()
                Cte = minidom.parse(doc)

            evCancCTe = Cte.getElementsByTagName('evCancCTe')

            if evCancCTe:
                chCTe = Cte.getElementsByTagName('chCTe')
                tpEvento = Cte.getElementsByTagName('tpEvento')
                xEvento = Cte.getElementsByTagName('xEvento')
                lista.append(
                    [chCTe[0].firstChild.data,
                    tpEvento[0].firstChild.data,
                    xEvento[0].firstChild.data]
                )
                #print(lista)

            else:

                # Chave CTE
                chCTe = Cte.getElementsByTagName('chCTe')

                # dhEmi
                dhEmi = Cte.getElementsByTagName('dhEmi')

                # dProg
                dProg = Cte.getElementsByTagName('dProg')

                # nCT
                nCT = Cte.getElementsByTagName('nCT')

                # tpCTe 
                tpCTe = Cte.getElementsByTagName('tpCTe')
            
                # tpServ
                tpServ = Cte.getElementsByTagName('tpServ')

                # tpEmis
                tpEmis = Cte.getElementsByTagName('tpEmis')

                # cMunIni
                cMunIni = Cte.getElementsByTagName('cMunIni')

                # xMunIni
                xMunIni = Cte.getElementsByTagName('xMunIni')
            
                # UFIni
                UFIni = Cte.getElementsByTagName('UFIni')

                # cMunFim
                cMunFim = Cte.getElementsByTagName('cMunFim')

                # xMunFim
                xMunFim = Cte.getElementsByTagName('xMunFim')
            
                # UFFim
                UFFim = Cte.getElementsByTagName('UFFim')

                # Valor CTE
                vTPrest = Cte.getElementsByTagName('vTPrest')

                # Valor da carga
                vCarga = Cte.getElementsByTagName('vCarga')


                # Chave NF
                if tpCTe[0].firstChild.data == '0':
                    try:
                        chaveNF = Cte.getElementsByTagName('chave')
                    except:
                        chaveNF = Cte.getElementsByTagName('chave')[0].firstChild.data
                    
                    if chaveNF:
                        for chave in chaveNF:
                            lista.append([ chCTe[0].firstChild.data, 
                                                        dhEmi[0].firstChild.data, 
                                                        dProg[0].firstChild.data if dProg else None, 
                                                        nCT[0].firstChild.data, 
                                                        tpCTe[0].firstChild.data, 
                                                        tpServ[0].firstChild.data, 
                                                        tpEmis[0].firstChild.data,
                                                        cMunIni[0].firstChild.data, 
                                                        xMunIni[0].firstChild.data, 
                                                        UFIni[0].firstChild.data,
                                                        cMunFim[0].firstChild.data, 
                                                        xMunFim[0].firstChild.data, 
                                                        UFFim[0].firstChild.data,
                                                        vTPrest[0].firstChild.data, 
                                                        vCarga[0].firstChild.data, 
                                                        chave.firstChild.data])
                    else:
                        nDoc = Cte.getElementsByTagName('nDoc')
                        for doc in nDoc:
                            lista.append([ chCTe[0].firstChild.data, 
                            dhEmi[0].firstChild.data, 
                            dProg[0].firstChild.data if dProg else None, 
                            nCT[0].firstChild.data, 
                            tpCTe[0].firstChild.data, 
                            tpServ[0].firstChild.data, 
                            tpEmis[0].firstChild.data,
                            cMunIni[0].firstChild.data, 
                            xMunIni[0].firstChild.data, 
                            UFIni[0].firstChild.data,
                            cMunFim[0].firstChild.data, 
                            xMunFim[0].firstChild.data, 
                            UFFim[0].firstChild.data,
                            vTPrest[0].firstChild.data, 
                            vCarga[0].firstChild.data, 
                            doc.firstChild.data])
                            
                else:
                    for ch in chCTe:
                        if ch.parentNode.nodeName == 'infCteComp':
                            chaveNF = ch.firstChild.data
                        else:
                            chCTe = ch.firstChild.data
                        
                    lista.append([ chCTe, 
                                                dhEmi[0].firstChild.data, 
                                                dProg[0].firstChild.data if dProg else None, 
                                                nCT[0].firstChild.data, 
                                                tpCTe[0].firstChild.data, 
                                                tpServ[0].firstChild.data, 
                                                tpEmis[0].firstChild.data,
                                                cMunIni[0].firstChild.data, 
                                                xMunIni[0].firstChild.data, 
                                                UFIni[0].firstChild.data,
                                                cMunFim[0].firstChild.data, 
                                                xMunFim[0].firstChild.data, 
                                                UFFim[0].firstChild.data,
                                                vTPrest[0].firstChild.data, 
                                                0, 
                                                chaveNF])

                
        
        return lista

    def criardf(self, lista):
        try:
            if len(lista[0]) == 3:
                nomes_colunas = ['chCTe', 'tpEvento', 'xEvento']
                tabtratada = pd.DataFrame(lista, columns=nomes_colunas)

                print(tabtratada)
                insert_dataframe_into_sql_server(tabtratada, 'Servidor', 'Banco de Dados', 'Login', 'SenhaBD', 'TabelaEventoCancelamento')


            else:
                nomes_colunas = ['chCTe', 'dhEmi', 'dProg', 'nCT', 'tpCTe', 'tpServ', 'tpEmis', 'cMunIni', 'xMunIni', 'UFIni', 'cMunFim', 'xMunFim', 'UFFim', 'vTPrest', 'vCarga', 'chaveNF']
                tabtratada = pd.DataFrame(lista,columns=nomes_colunas)

                tabtratada['dhEmi'] = tabtratada['dhEmi'].astype(str)

                # Extrair a parte da data/hora que é reconhecida
                tabtratada['dhEmi'] = tabtratada['dhEmi'].str.extract(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})')

                # Converter a coluna 'dhEmi' para DateTime
                tabtratada['dhEmi'] = pd.to_datetime(tabtratada['dhEmi'], format='%Y-%m-%dT%H:%M:%S')

                # Formatar a coluna 'dhEmi' no formato desejado
                #df['dhEmi'] = df['dhEmi'].dt.strftime('%d/%m/%Y %H:%M:%S')

                tabtratada['dProg'] = pd.to_datetime(tabtratada['dProg'], format='%Y-%m-%d')

                print(tabtratada)
                insert_dataframe_into_sql_server(tabtratada, 'Servidor', 'Banco de Dados', 'Login', 'SenhaBD', 'TabelaCTE')

        except:
            print(f'***/n{lista}/n***')
    
def insert_dataframe_into_sql_server(dataframe, server, database, username, password, table_name):
    try:
        # Crie uma string de conexão com o SQL Server
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        # Estabeleça a conexão com o banco de dados
        conn = pyodbc.connect(connection_string)

        # Use o método to_sql para inserir o DataFrame na tabela do banco de dados
        cursor = conn.cursor()
        for _, row in dataframe.iterrows():
            insert_query = f"INSERT INTO {table_name} ({', '.join(dataframe.columns)}) VALUES ({', '.join(['?']*len(dataframe.columns))})"
            cursor.execute(insert_query, tuple(row))
        conn.commit()

        # Feche a conexão com o banco de dados
        conn.close()

        print(f'DataFrame inserido com sucesso na tabela {table_name}.')
    except Exception as e:
        print(f'Ocorreu um erro ao inserir o DataFrame na tabela {table_name}: {str(e)}')

def monitorar_pasta(origem):
    event_handler = FileHandler(origem)
    observer = Observer()
    observer.schedule(event_handler, path=origem, recursive=False)
    observer.start()

    print(f'Monitorando a pasta {origem}...')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    pasta_origem = r'.\pastaxmls'
    monitorar_pasta(pasta_origem)

