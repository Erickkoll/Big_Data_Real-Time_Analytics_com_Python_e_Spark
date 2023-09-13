# Lab 6 - Análise de Dados em Tempo Real com Apache Spark Structured Streaming
# https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html

# Funções
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

# Sessão
spark = SparkSession.builder.appName("StructuredNetworkWordCount").getOrCreate()

# Criamos um DataFrame para o Stream que vai extrair os dados em tempo real do gerador de dados em localhost:9999
lines = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()

# Divide cada linha de dados em palavras
words = lines.select(explode(split(lines.value, " ")).alias("word"))

# Contador de palavras
wordCounts = words.groupBy("word").count()

 # Executa a query em tempo real e imprime a contagem de palavras em tempo real
query = wordCounts.writeStream.outputMode("complete").format("console").start()

# Aguarda término da conexão
query.awaitTermination()
