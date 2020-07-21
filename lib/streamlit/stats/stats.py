# Copyright 2018-2020 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gprof2dot
import io

import streamlit as st


@st.cache
def graph(node_thresh=0.5, edge_thresh=0.1, theme="color"):
    profile = gprof2dot.PstatsParser("out.pstats").parse()
    output = io.StringIO()
    dot = gprof2dot.DotWriter(output)

    dot.show_function_events = [
        gprof2dot.labels[nam] for nam in gprof2dot.defaultLabelNames
    ]

    profile.prune(node_thresh / 100, edge_thresh / 100, [], False)
    dot.graph(profile, gprof2dot.themes[theme])
    return output.getvalue()


def run():
    st.header("Stats")
    theme = st.sidebar.selectbox("Theme", tuple(gprof2dot.themes.keys()))
    node_thresh = st.sidebar.slider(
        "Node threshold", value=0.5, step=0.01, max_value=5.0
    )
    edge_thresh = st.sidebar.slider(
        "Edge threshold", value=0.1, step=0.01, max_value=5.0
    )
    chart = graph(node_thresh, edge_thresh, theme)
    st.graphviz_chart(chart)


if __name__ == "__main__":
    run()
