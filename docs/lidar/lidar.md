# Light Detection and Ranging (LiDAR)


Light Detection and Ranging (*LiDAR* or *lidar*) uses laser pulses to measure earth surface properties such as canopy or terrain elevation. The laser pulses are sent from a remote sensing platform (fix station or airborne) to surfaces, which reflect the pulses with different speed (time-of-flight informs about terrain elevation) and energy pattern (leaves behave differently than rock). In its raw form, lidar data is a point cloud with various, geo-referenced information about the reflected signal. Lidar point clouds are typically stored in *las* format or compressed *laz* format. *las*-formatted data are much faster to process, but also much larger than *laz*-formatted data. For this reason, lidar data are preferably transferred in *laz* format, while the *las* format is preferably used for processing lidar data.

* Use the free tool [*lasZIP*](https://rapidlasso.com/laszip/) to convert *laz* to *las* datasets.


