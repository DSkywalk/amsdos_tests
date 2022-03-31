# amsdos_tests

The idea is to be able to add machine code to a basic amsdos file. Our extra machine-code data is:

```00 00 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 00 00 00```

The `example.bas` file contains extra bytes that will not be stored in the amstrad's memory because the length of the BASIC text is **14 (0xe)** bytes.

![imagen](https://user-images.githubusercontent.com/560310/161132454-92478056-cce9-47c3-82a8-e409224d17aa.png)
_cpc memory dumps just with the BASIC DATA_

But if we patch the header with the total size **36 (0x24)** bytes
```
./amsdos_length_hack.py example.bas 36 h3.bas
```
Finally add BAS binary using iDSK:
```
./iDSK test.dsk -i h3.bas -t 1
```

![imagen](https://user-images.githubusercontent.com/560310/161133754-03d2d532-25ae-4bb1-8339-ccb3ed960f69.png)

voila!
