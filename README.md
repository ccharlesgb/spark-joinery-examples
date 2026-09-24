# Spark Joinery Examples

This repo contains a collection of example pipelines for the spark-joinery package

---

**Repository**: [https://github.com/ccharlesgb/spark-joinery](https://github.com/ccharlesgb/spark-joinery)

**Documentation**: [https://ccharlesgb.github.io/spark-joinery/](https://ccharlesgb.github.io/spark-joinery/)

---

# Setup

Ensure you have uv and then run:

```sh
just install
```

# Running Examples

To run an example pipeline, navigate to the root of the repository and use the `just` command with the `run-example` target followed by the name of the example directory. For instance:

```sh
just run-example order_product_example/
```
 
Or just the package name:

```sh
just run-example order_product
```