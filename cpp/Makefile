PRG		=bbmagic_server
BBM_LIB		=bbmagic_lib_2.0
ONEWIRE         =onewire_server

all: clean
	g++ -o $(PRG) $(PRG).cxx ./bbmagic/libs/$(BBM_LIB).a ./bbmagic/libs/libbluetooth.a -lrt
	g++ -std=c++17 -o $(ONEWIRE) $(ONEWIRE).cxx -lstdc++fs

clean:
	rm -f $(PRG)

