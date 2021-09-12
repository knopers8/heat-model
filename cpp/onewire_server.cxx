
#include <iostream>
#include <filesystem>
#include <fstream>
#include <chrono>

#include "influxdb-cpp/influxdb.hpp"



int main(int argc, char** argv)
{
  if (argc != 5) {
    std::cerr << "Arguments number different than 4. Expected arguments: dbname login password period_seconds" << std::endl;
    return 1;
  }

  influxdb_cpp::server_info si("127.0.0.1", 8086, argv[1], argv[2], argv[3]);

  int64_t periodSeconds = std::stoll(argv[4]);
  if (periodSeconds < 1) {
    std::cerr << "Readout period is incorrect: " << argv[4] << std::endl;
    return 2;
  }

  constexpr auto sensorPath = "/sys/bus/w1/devices/28-00000d4a1c31/temperature";

  size_t failedTimesInARow = 0;
  auto startTime = std::chrono::system_clock::now();
  auto lastReadoutTime = startTime;
  while (failedTimesInARow < 5) {
    // == Rate limiter ==
    auto now = std::chrono::system_clock::now();
    auto timeToUSleep = periodSeconds * 1000000 - std::chrono::duration<double, std::micro>(now - lastReadoutTime).count();
    usleep(static_cast<uint64_t>(timeToUSleep));

    // == Readout ==
    lastReadoutTime = std::chrono::system_clock::now();

    // For some reason, ifstream will open a file even if it does not exist. Thus I check if it exists each time.
    if (!std::filesystem::exists(sensorPath)){
      std::cerr << "The path to the sensor temperature readout does not exist, check if the sensor is connected and one wire is enabled" << std::endl;
      failedTimesInARow++;
      continue;
    }

    // fixme: opening a file each time is probably stupid.
    std::ifstream readout(sensorPath);
    if (!readout.is_open()) {
      std::cerr << "Could not open the sensor readout file" << std::endl;
      failedTimesInARow++;
      continue;
    }

    std::string valueAsString;
    readout >> valueAsString;
    readout.close();
    if (valueAsString.empty()) {
      std::cerr << "Value read from file is empty" << std::endl;
      failedTimesInARow++;
      continue;
    }
    failedTimesInARow = 0;

    std::cout << "temperature: " << valueAsString << std::endl;

    // == Storage == 
    double value = std::stoull(valueAsString.c_str()) / 1000.0;
    auto workTime = std::chrono::duration<double>(std::chrono::system_clock::now() - startTime).count();

    influxdb_cpp::builder()
            .meas("onewire")
            .tag("address", "28-00000d4a1c31") // fixme: if i need more than one sensor, this should be done properly
            .field("temperature", value)
            .field("rate", periodSeconds)
            .field("work_time", workTime)
            .post_http(si);

  }

  return failedTimesInARow >= 5 ? 4 : 0;
}
