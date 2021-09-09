PRG		=bbmagic_server
BBM_LIB		=bbmagic_lib_2.0

all: clean
	g++ -o $(PRG) $(PRG).cxx ./bbmagic/libs/$(BBM_LIB).a ./bbmagic/libs/libbluetooth.a -lrt

clean:
	rm -f $(PRG)

