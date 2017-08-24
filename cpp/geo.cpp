#include <iostream>
#include <math.h>
#include <stdio.h>
#include <string.h>

using namespace std;

#define DEGREE_TO_RADIANS		0.0174533f
#define EARTH_RADIUS			6371.f

int population[3] = {1000, 1000, 100};
float latitudes[3] = {0.1f, 0.1f, 45.3f};
float longitudes[3] = {0.2f, 0.3f, 45.5f};

int *output;

float geo_distance(float lat1, float lon1, float lat2, float lon2)
{
	float lat2r = lat2 * DEGREE_TO_RADIANS;
	float lat1r = lat1 * DEGREE_TO_RADIANS;

	float dist_lat = (lat2 - lat1) * DEGREE_TO_RADIANS;
	float dist_lon = (lon2 - lon1) * DEGREE_TO_RADIANS;
	float s_lat = 1.0f * sin(dist_lat / 2);
	float s_lon = 1.0f * sin(dist_lon / 2);

	float inter = s_lat * s_lat + cos(lat1r) * cos(lat2r) * s_lon * s_lon;
	return 2 * EARTH_RADIUS * atan2(sqrt(inter), sqrt(1 - inter));
}

void do_work(int index, float kmrange)
{
	float my_lat = latitudes[index];
	float my_lon = longitudes[index];

	printf("[%d][%d]\n", index, output[index]);



	for (size_t i = index + 1; i < 3; i++) {
		float to_lat = latitudes[i];
		float to_lon = longitudes[i];

		float dist = geo_distance(my_lat, my_lon, to_lat, to_lon);

		if (dist <= kmrange) {
			output[index] += population[i];
			output[i] += population[index];
		}
	}
}

int main(int argc, char const *argv[])
{
	float kmrange = 50.0f;

	output = new int[3];
	memset(output, 0, 3);

	for (size_t i = 0; i < 3; i++) {
		do_work(i, kmrange);
	}

	for (size_t i = 0; i < 3; i++) {
	cout << output[i] << "\n";
	}

	return 0;
}
