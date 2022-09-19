from __future__ import annotations
from importlib.metadata import metadata
import os
import sys

from .helpers import helm_template


def test_required_resources():
    config = """
kaniko:
  serviceAccount:
    create: true
  roleArn: AWSIRSARoleKaniko
    """

    r = helm_template(config)

    assert "edp-kaniko" in r["serviceaccount"]
    assert "AWSIRSARoleKaniko" in r["serviceaccount"]["edp-kaniko"]["metadata"]["annotations"]["eks.amazonaws.com/role-arn"]

    assert "tekton-triggers-sa-ns" in r["serviceaccount"]

    assert "tekton-triggers-eventlistener-binding-ns" in r["rolebinding"]
    assert "ns" in r["rolebinding"]["tekton-triggers-eventlistener-binding-ns"]["metadata"]["namespace"]
    assert "ns" in r["rolebinding"]["tekton-triggers-eventlistener-binding-ns"]["subjects"][0]["namespace"]

    assert "tekton-triggers-eventlistener-clusterbinding-ns" in r["clusterrolebinding"]
    assert "ns" in r["clusterrolebinding"]["tekton-triggers-eventlistener-clusterbinding-ns"]["subjects"][0]["namespace"]


def test_ingress_for_gitlab_el():
    config = """
global:
  dnsWildCard: "example.com"
gitlab:
  enabled: true
    """

    el_Name = "el-gitlab-listener"
    r = helm_template(config)

    assert el_Name in r["ingress"]
    assert "event-listener-ns.example.com" in r["ingress"][el_Name]["spec"]["rules"][0]["host"]
    assert el_Name in r["ingress"][el_Name]["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"]["name"]


def test_ingress_for_github_el():
    config = """
global:
  dnsWildCard: "example.com"
github:
  enabled: true
    """

    el_Name = "el-github-listener"
    r = helm_template(config)

    assert el_Name in r["ingress"]
    assert "event-listener-ns.example.com" in r["ingress"][el_Name]["spec"]["rules"][0]["host"]
    assert el_Name in r["ingress"][el_Name]["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"]["name"]
