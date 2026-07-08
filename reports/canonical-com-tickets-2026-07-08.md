# Ticketable copy fixes – canonical.com
**Date:** 2026-07-08
**Pages scanned:** 40
**Candidates:** 84

Every item below is an exact find→replace. Judgement-call findings (including flowery-language) are excluded from this list entirely.

**Review before submitting:** check the box for each fix you approve, commit this file, then run:

```
python3 scripts/ticketable.py --approve reports/canonical-com-tickets-2026-07-08.md --save
```

Unchecked items are treated as rejected and will not be submitted.

---

**By rule:** uk-spelling (46), product-names (16), punctuation (13), number-formatting (7), house-style (2)

---

## `/data/cassandra`

- [ ] `e281c9d8fa89` **Run Apache Cassandra across public and private clouds** | [product-names] `VMWare` → `VMware`

## `/data/kafka`

- [ ] `a5b8ed24af00` **Run Kafka on any public, private, or hybrid cloud** | [product-names] `VMWare` → `VMware`

## `/data/kafka/managed`

- [ ] `93039db3101f` **Managed Kafka by Canonical** | [uk-spelling] `data centre` → `data center`
- [ ] `ad51658c9159` **Secure by design** | [uk-spelling] `Minimise` → `Minimize`
- [ ] `5cc7b5c404e7` **Secure by design** | [number-formatting] `27001` → `27,001`
- [ ] `c4edd95c393f` **Turnkey service** | [uk-spelling] `data centre` → `data center`
- [ ] `5f18771fee55` **Managed Kafka on OpenStack** | [uk-spelling] `data centre` → `data center`
- [ ] `627c30f39a39` **Managed Kafka resources** | [punctuation] ` - ` → ` – `
- [ ] `662b0324317c` **Managed Kafka resources** | [house-style] `white paper` → `whitepaper`

## `/data/kafka/support`

- [ ] `daee5f33e843` **Go further** | [uk-spelling] `data centre` → `data center`
- [ ] `053d57b8e0c3` **Kafka platform deployment service** | [uk-spelling] `data centre` → `data center`

## `/data/kafka/what-is-kafka`

- [ ] `7e6369fd0e0a` **Durable** | [uk-spelling] `minimised` → `minimize`
- [ ] `7a92837fbca8` **Charmed Kafka** | [uk-spelling] `data centre` → `data center`
- [ ] `8fe8d8111242` **Kafka consultancy and support** | [uk-spelling] `data centre` → `data center`

## `/data/lakehouse`

- [ ] `1887d9aa3eb3` **Apache Spark ®** | [punctuation] `—` → ` – `

## `/data/mysql`

- [ ] `9ffad056c3f6` **Run MySQL on any public, private or hybrid cloud** | [uk-spelling] `data centre` → `data center`
- [ ] `0fbed664e9b9` **Run MySQL on any public, private or hybrid cloud** | [uk-spelling] `optimised` → `optimize`
- [ ] `c7232d644651` **Run MySQL on any public, private or hybrid cloud** | [product-names] `VMWare` → `VMware`
- [ ] `b3410b0e48ed` **From $3099** | [uk-spelling] `data centre` → `data center`
- [ ] `8e92653df3d6` **[PostgreSQL vs MySQL webinar](https://www.linkedin.com/events/choosingbetweenthemostpopularop7094241865746542592/theater/)** | [product-names] `open-source` → `open source`

## `/data/mysql/managed`

- [ ] `74e72bde9454` **Managed MySQL on your cloud** | [product-names] `VMWare` → `VMware`
- [ ] `0ffc0c143a40` **Service delivery with security in mind.** | [number-formatting] `27001` → `27,001`

## `/data/mysql/support`

- [ ] `4e2f13212491` **[PostgreSQL vs MySQL webinar](https://ubuntu.com/engage/postgresql-mysql)** | [product-names] `open-source` → `open source`

## `/data/opensearch`

- [ ] `31073d417e33` **Run OpenSearch on any public, private or hybrid cloud** | [uk-spelling] `data centre` → `data center`
- [ ] `f328f9a9169e` **Run OpenSearch on any public, private or hybrid cloud** | [product-names] `Microcloud` → `MicroCloud`
- [ ] `a47c93d049fc` **Run OpenSearch on any public, private or hybrid cloud** | [product-names] `VMWare` → `VMware`
- [ ] `5b6181cb7f33` **From $3099** | [uk-spelling] `centre` → `center`
- [ ] `69e170fb0a56` **OpenSearch use cases** | [product-names] `open-source` → `open source`

## `/data/opensearch/managed`

- [ ] `0e44bd896031` **1. Deployment** | [uk-spelling] `Specialised` → `Specialize`
- [ ] `c6017c80af21` **Key features** | [uk-spelling] `Minimise` → `Minimize`
- [ ] `7fc91e7affe4` **Key features** | [number-formatting] `27001` → `27,001`
- [ ] `f90ce8e82e68` **Key features** | [uk-spelling] `data centre` → `data center`
- [ ] `dcb816486dba` **$9470** | [uk-spelling] `data centre` → `data center`

## `/data/opensearch/support`

- [ ] `8c76098b5e23` **Full-stack support** | [punctuation] `—` → ` – `
- [ ] `a6d7e555cce6` **Go further** | [uk-spelling] `data centre` → `data center`
- [ ] `dd5e3f75f25d` **OpenSearch platform deployment service** | [uk-spelling] `data centre` → `data center`

## `/data/opensearch/what-is-opensearch`

- [ ] `0ddd17d2db87` **The flexibility of open source** | [uk-spelling] `customise` → `customize`
- [ ] `399f4aa6e46b` **Search engine** | [uk-spelling] `organise` → `organize`
- [ ] `80e7294becdc` **OpenSearch plugins** | [uk-spelling] `optimise` → `optimize`
- [ ] `081621faebeb` **Charmed OpenSearch** | [uk-spelling] `data centre` → `data center`
- [ ] `cd9aebfe49e1` **Advanced professional services for OpenSearch, when you need them** | [uk-spelling] `data centre` → `data center`
- [ ] `4c8e12782d1b` **Learn more about Opensearch** | [uk-spelling] `utilise` → `utilize (or better: use)`

## `/data/relational-databases`

- [ ] `ddf40361a8f5` **A system for managing digital information** | [uk-spelling] `organise` → `organize`
- [ ] `3999c453801c` **When you can’t afford to lose data** | [uk-spelling] `favour` → `favor`
- [ ] `1733238d6049` **When the size of your data matters** | [uk-spelling] `optimised` → `optimize`
- [ ] `e8417b1fb5f2` **When you have dynamic or changing access patterns** | [uk-spelling] `optimised` → `optimize`
- [ ] `0496b4fa4f51` **When you would like to centralise your data management** | [uk-spelling] `centralise` → `centralize`
- [ ] `e986e3ab2987` **When you would like to centralise your data management** | [uk-spelling] `specialised` → `specialize`
- [ ] `ff31d188c093` **When you would like to centralise your data management** | [uk-spelling] `specialised` → `specialize`
- [ ] `c19ea425e81a` **1969** | [uk-spelling] `specialised` → `specialize`
- [ ] `7bf604a2f231` **[SQL** | [uk-spelling] `optimised` → `optimize`
- [ ] `ff27ff03140e` **From our blog** | [product-names] `open-source` → `open source`

## `/data/spark/managed`

- [ ] `968a71ba9c41` **Managed Spark by Canonical** | [uk-spelling] `data centre` → `data center`
- [ ] `14518059578c` **Secure by design** | [number-formatting] `27001` → `27,001`
- [ ] `fd73a753d797` **Turnkey service** | [uk-spelling] `data centre` → `data center`
- [ ] `eba84b941f84` **$9470** | [uk-spelling] `data centre` → `data center`
- [ ] `ad2da6014005` **[Build an online datahub with Spark](https://ubuntu.com/engage/spark_online_data_hub)** | [house-style] `white paper` → `whitepaper`

## `/data/spark/support`

- [ ] `83db38c6518e` **Go further** | [uk-spelling] `data centre` → `data center`
- [ ] `471d4a49b7a0` **Spark data lake platform deployment service** | [uk-spelling] `data centre` → `data center`

## `/data/warehouse`

- [ ] `eb7ed7b99a19` **OLAP vs OLTP** | [uk-spelling] `optimised` → `optimize`

## `/microk8s/compare`

- [ ] `2167ec87fe92` **Compare features** | [number-formatting] `540 MB` → `540MB`
- [ ] `54765708baf4` **Compare features** | [number-formatting] `512 MB` → `512MB`
- [ ] `75c295c0ad1f` **Compare features** | [number-formatting] `644 MB` → `644MB`
- [ ] `13e6b4f69d24` **Why MicroK8s?** | [punctuation] ` - ` → ` – `
- [ ] `6d19bb3f0379` **Webinars** | [punctuation] `—` → ` – `

## `/microk8s/features`

- [ ] `03aafbb945bf` **High availability (HA)** | [punctuation] ` - ` → ` – `
- [ ] `d08677090e42` **Strict confinement** | [uk-spelling] `minimise` → `minimize`
- [ ] `c36d1ce8b1f0` **NVIDIA GPU support, ideal for AI/ML and HPC** | [uk-spelling] `optimised` → `optimize`
- [ ] `a9e74efea075` **Custom launch configurations** | [punctuation] ` - ` → ` – `
- [ ] `062618066725` **Better user experience with addons** | [punctuation] `—` → ` – `
- [ ] `b7c382b65b1c` **Better user experience with addons** | [uk-spelling] `favourite` → `favorite`

## `/microk8s/resources`

- [ ] `8ae09efe9e51` **[Kubernetes: a secure,** | [uk-spelling] `optimise` → `optimize`

## `/microk8s/tutorials`

- [ ] `e22780a0bcf2` **[Install a local** | [product-names] `open-source` → `open source`

## `/mlops`

- [ ] `645b41fcc6f6` **Charmed MLFlow** | [punctuation] ` - ` → ` – `

## `/mlops/kubeflow/what-is-kubeflow`

- [ ] `761f8deabad0` **More...** | [punctuation] ` - ` → ` – `
- [ ] `2e7d7bb408ca` **MLOps at any scale** | [punctuation] ` - ` → ` – `
- [ ] `3e40c5cd6843` **Who uses Kubeflow?** | [punctuation] ` - ` → ` – `
- [ ] `9e795ed35e0d` **Who uses Kubeflow?** | [punctuation] ` - ` → ` – `

## `/mlops/mlops-workshop`

- [ ] `34a8f97ef49b` **Learn from experts in the industry** | [product-names] `open-source` → `open source`

## `/observability/managed`

- [ ] `a7e4ba026050` **Managed Open Source Observability** | [product-names] `Open Source` → `open source`
- [ ] `69a04d27b1a8` **No lock-in** | [product-names] `open-source` → `open source`
- [ ] `c1369865e510` **Reliable monitoring tools you can count on** | [product-names] `Extended Security Maintenance` → `Expanded Security Maintenance`
- [ ] `3b467bd7c236` **Reliable monitoring tools you can count on** | [product-names] `open-source` → `open source`
- [ ] `3e11d87a1040` **Contact us about Managed Observability** | [uk-spelling] `Data Centre` → `Data Center`

