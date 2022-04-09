# amsdos hacks

Python utilities used to fix the games for [clean-cpc-db](https://archive.org/details/amstrad-cpc-clean-db). Explanation and usage also [in Spanish on youtube](youtu.be/qNPGfHlZm5g).

## amsdos_length_hack (deprecated)

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

## amsdos_append_hack

The idea is the same that length_hack, to be able to add machine code to a basic amsdos file. But has a better result:

Params
* source-bas-path: Original binary BASIC file to append the extra binary.
* source-bin-path: New binary machine code to be append.
* hex-address-append: The position in source-bas where the source-binary will be attached (into BASIC).
* hex-token-exe: If your BASIC contains a "CALL &FEA5" it will substitute that memory address (0xFEA5) with the one you specify here. If not found, it does nothing.
* out-file: Name of the destination file generated.

```
example:
$ ./amsdos_append_hack.py LOADER.BAS FIXEDCRACK.BIN 0x50b 0x0170 NEWLOADER.BAS
```

## amsdos_fix_checksum

Recalculates the checksum signature of the AMSDOS header.

Params:
* source-bas-path: Original binary BASIC file to fix checksum.
* dest-bas-path: Name of the destination file generated.

```
example:
$ ./amsdos_fix_checksum.py LOADER.BAS FIXLOADER.BAS
```




