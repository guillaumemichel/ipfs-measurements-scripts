# Hydras Dial Down scripts

This work has been cancelled. The purpose was to study the behavior of the DHT routing tables after the hydras leave the DHT. However, they will continue participating in the DHT, hence this study doesn't make sense for now.

These scripts could be useful in the future, if we decide to remove the Hydras completely. This will require further work to get the scripts working.

## Plots that we want

1. Diversity over time. Number of distinct peers per bucket. Take a few (~3) buckets (group the bars together per crawl_id), and plot their diversity (y axis) over time (x axis)
2. Number of peers per routing table over time. Boxplot of the number of peers (y axis) inside each peers routing table, for each crawl (x axis).
3. Number of peers per bucket. Take a few (~3) buckets (group the bars together per crawl_id), and plot the average number of peerids inside each bucket (y axis) over time (x axis).
4. Number of known peers among the 2 closest over time. Boxplot
5. Offline peers ratio over time. Simple bars chart
6. Offline peers ratio per bucket over time. same as above
7. Missing peers per bucket over time. ~3 buckets, and plot the average number of missing peers over time.
