# Recommender System Analysis
This repository is used to calculate two major metrics of the Recommender System UI testing app:
- Task Completion Time (TCT)
- Click-Through-Rate (CTR)

## Related repositories

- [recommender-system-ui](https://github.com/justinsj/recommender-system-ui): Main Amazon-like React Native testing app
- [recommender-system-scraper](https://github.com/justinsj/recommender-system-scraper): Scripts to obtain data from Amazon

## Example Results

```
average_ctrs_df:
    interfaceId       ctr
0      control  0.000000
1   large_long  0.058463
2  large_short -0.010000
3   small_long -0.010952
4  small_short  0.020168
average_tcts_df:
    interfaceId      tct
0      control   0.0000
1   large_long  29.2979
2  large_short   8.6066
3   small_long   2.3894
4  small_short  14.2318
average ctr:  0.21142857142857138
average tct:  51.4721
```

## Cite

To cite this project, please consider using the following bibtex:
```
@misc{recommender-system-analysis,
  author = {San Juan, Justin and Chambers, Owen},
  title = {Tailoring Product Recommendations for Mobile Devices},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/justinsj/recommender-system-analysis}},
}
```
