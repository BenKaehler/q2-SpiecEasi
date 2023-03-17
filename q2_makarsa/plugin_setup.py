from networkx import Graph, read_graphml, write_graphml
from q2_types.feature_table import FeatureTable, Frequency
from qiime2.plugin import Bool, Float, Int, Metadata, Plugin, Str

from ._network import Network, NetworkDirectoryFormat, NetworkFormat
from ._spieceasi import spiec_easi
from ._flashweave import flashweave
from ._visualisation import visualise_network

plugin = Plugin(
    name="makarsa",
    version="0.0.0-dev",
    website="https://github.com/BenKaehler/q2-makarsa",
    package="q2_makarsa",
    description=(
        "This QIIME 2 plug-in provides biological network analysis and "
        "visualisation and may be useful to anybody who wants to infer "
        "graphical models for all sorts of compositional "
        "data, though primarily intended for microbiome "
        "relative abundance data (generated from 16S "
        "amplicon sequence data)."
    ),
    short_description="A QIIME 2 plugin to expose some SpiecEasi "
    "functionality.",
    # citations=qiime2.plugin.Citations.load(
    #    'citations.bib', package='q2_dada2'
)

plugin.register_semantic_types(Network)
plugin.register_formats(NetworkDirectoryFormat, NetworkFormat)
plugin.register_semantic_type_to_format(
    Network, artifact_format=NetworkDirectoryFormat
)


@plugin.register_transformer
def _1(network: Graph) -> NetworkFormat:
    ff = NetworkFormat()
    write_graphml(network, str(ff))
    return ff


@plugin.register_transformer
def _2(ff: NetworkFormat) -> Graph:
    return read_graphml(str(ff))


plugin.visualizers.register_function(
    function=visualise_network,
    inputs={"network": Network},
    parameters={"metadata": Metadata},
    name="Visualize network",
    description="Create an interactive depiction of your network.",
)


plugin.methods.register_function(
    function=spiec_easi,
    inputs={"table": FeatureTable[Frequency]},
    parameters={
        "method": Str,
        "lambda_min_ratio": Float,
        "nlambda": Int,
        "rep_num": Int,
        "ncores": Int,
        "thresh": Float,
        "subsample_ratio": Float,
        "seed": Float,
        "sel_criterion": Str,
        "verbose": Bool,
        "pulsar_select": Bool,
        "lambda_log": Bool,
        "lambda_min": Float,
        "lambda_max": Float,
    },
    outputs=[("network", Network)],
    input_descriptions={
        "table": (
            "All sorts of compositional data though primarily intended "
            "for microbiome relative abundance data "
            "(generated from 16S amplicon sequence data)"
        )
    },
    parameter_descriptions={
        "method": "Methods available for spieceasi,for example mb,glasso,slr",
        "lambda_min_ratio": (
            "Input parameter of spieceasi which represents "
            "the scaling factor that determines the minimum "
            "sparsity/lambda parameter"
        ),
        "nlambda": "Input parameter of spieceasi ",
        "rep_num": "Input parameter of spieceasi ",
        "ncores": "Number of cores for parallel computation",
        "thresh": "Threshold for StARS criterion",
        "subsample_ratio": "Subsample size for StARS",
        "seed": "Set the random seed for subsample set",
        "sel_criterion": "Specifying criterion/method for model selection, "
        "Accepts 'stars' [default], 'bstars' (Bounded StARS)",
        "verbose": "Print extra output [default]",
        "pulsar_select": "Perform model selection",
        "lambda_log": "lambda.log should values of lambda be distributed "
        "logarithmically (TRUE) or linearly (FALSE) between "
        "lamba.min and lambda.max",
    },
    output_descriptions={"network": "The inferred network"},
    name="SpiecEasi",
    description=(
        "This method generates the sparse matrix of network of input " "data"
    ),
)


plugin.methods.register_function(
    function=flashweave,
    inputs={"table": FeatureTable[Frequency]},
    parameters={
        "meta_data":  Metadata,
        "pca_dimension": Int,
        "min_cluster_size": Int,
        "max_cluster_size": Int,
        "n_threads": Int,
        "seed": Int,
        "alpha": Float,
        "nruns": Int,
        "subsample_ratio": Float,
        "num_clusters": Int,
        "max_overlap": Float,
        "verbose": Bool
    },
    outputs=[("network", Network)],
    input_descriptions={
        "table": (
            "All sorts of compositional data though primarily intended "
            "for microbiome relative abundance data "
            "(generated from 16S amplicon sequence data)")
    },
    parameter_descriptions={
        "meta_data": "a pathe which contain file ofmeta data of input data",
        "pca_dimension": "PCA dimension (default: 10)",
        "min_cluster_size": "minimum cluster size (default: 2)",
        "max_cluster_size": "maximum cluster size (default: 50)",
        "n_threads": "number of threads to use (default: 1) ",
        "seed": "random seed (default: 1)",
        "alpha": "threshold used to determine statistical significance",
        "nruns": "flashweave parameter",
        "subsample_ratio": "flashweave parameter",
        "num_clusters": "flashweave parameter",
        "max_overlap": "flashweave parameter",
        "verbose": "Enable verbose output"
    },
    output_descriptions={"network": "The inferred network"},
    name="flashweave",
    description=(
        "FlashWeave predicts ecological interactions between microbes from "
        "large-scale compositional abundance data "
    ),
)