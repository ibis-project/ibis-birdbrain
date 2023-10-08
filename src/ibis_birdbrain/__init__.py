# imports
import os
import ibis
import marvin

import logging as log

from dotenv import load_dotenv

from ibis_birdbrain.bot import Bot
from ibis_birdbrain.systems import default
from ibis_birdbrain.filesystem import ingest_docs

# configure logging
log.basicConfig(
    level=log.WARN,
)


# load .env
load_dotenv()

# ai platform
# marvin.settings.llm_model = "openai/gpt-3.5-turbo-16k"
marvin.settings.llm_model = "openai/gpt-4"
marvin.settings.openai.api_key = os.getenv("OPENAI_API_KEY")  # type: ignore
marvin.settings.llm_max_tokens = 1000

# data platform
ibis.options.interactive = False
bb_con = ibis.connect("duckdb://md:birdbrain")
mem_con = ibis.connect("duckdb://")
tpch_con = ibis.connect("duckdb://md:tpch")
imdb_con = ibis.connect("duckdb://md:imdb")

data_cons = [bb_con, mem_con, tpch_con, imdb_con]
# configure docs
docs_path = "data/docs/"
ibis_docs = "ibis_docs"
ibis_tpc_docs = "ibis_tpc"
birdbrain_docs = "birdbrain_docs"

docs = [ibis_docs, ibis_tpc_docs, birdbrain_docs]

# ingest docs into docs con to use like any data con!
docs_con = ibis.connect("duckdb://birdbrain_docs.ddb")
ingest_docs(docs_path=docs_path, docs=docs, con=docs_con)

# bots
bot = Bot(docs_con=docs_con, data_cons=data_cons, system=default)

# __all__
__all__ = ["Bot", "bot"]
