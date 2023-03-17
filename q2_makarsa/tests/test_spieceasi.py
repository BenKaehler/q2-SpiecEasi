from networkx import read_graphml
import networkx.algorithms.isomorphism as iso
from qiime2.plugin.testing import TestPluginBase
import biom

from q2_makarsa._spieceasi import spiec_easi


class TestSpieceasi(TestPluginBase):
    package = "q2_makarsa.tests"

    def test_defaults(self):
        table = biom.load_table(self.get_data_path("table.biom"))
        observed = spiec_easi(table.to_dataframe().transpose(), rep_num=5)
        expected = read_graphml(self.get_data_path("network.graphml"))
        self.assertTrue(iso.is_isomorphic(observed, expected))