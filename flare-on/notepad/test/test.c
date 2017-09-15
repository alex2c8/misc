#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int MAGIC_HAPPENS_HERE(int *PE, LPVOID fileBegin) {
	int ret;
	HANDLE module;
	LPVOID moduleBegin;
	HANDLE fmh;
	int fs;
	int dm;
	
	char const str_key[] = "\\key.bin\0";
	char const str_flareon[] = "\\flareon2016challenge\0";
	char const str_where[] = "where\\s my key file?\0";
	char const str_what[] = "what\\s wrong with my key file?\0";

	
	
	module = CreateFile(L"C:\\Users\\student\\Desktop\\flare-on\\notepad\\notepad.exe", GENERIC_READ, 1, 0, 3, 0x80, 0);
	if (module == NULL) {
		printf("module: NOPE\n");
		return -1;
	}
	
	
	dm = GetLastError();
	fs = GetFileSize(module, NULL);
	fmh = CreateFileMapping(module, 0, 4, 0, fs, 0);
	moduleBegin = MapViewOfFile(fmh, 2, 0, 0, 0);
	printf("%d\n", dm);
	
	//if(*(int*)((char*)moduleBegin + 0xE8) == 0x48025287) {
	//	printf("OK, found in module\n");
	//}
	
	
	
	CloseHandle(module);
	return ret;
}

int main() {
	

	HANDLE fileHandle, fileMappingHandle;
	LPVOID fileBegin, fileBegin2;
	int fileSize, fszOut;
	int offset, *PE;
	int test1, test2;
	int ret;

	
	

	fileHandle = CreateFile("C:\\Users\\student\\flareon2016challenge\\bin2.exe", 0xC0000000, 0, 0, 3, 0x80, 0);
	if (fileHandle == NULL) {
		printf("NOPE\n");
		return -1;
	}


	fileSize = GetFileSize(fileHandle, &fszOut);
	
	fileMappingHandle = CreateFileMapping(fileHandle, 0, 4, 0, fileSize, 0);
	if (fileMappingHandle == NULL) {
		printf("fmh: NOPE\n");
		return -1;
	}
	
	fileBegin = MapViewOfFile(fileMappingHandle, 2, 0, 0, 0);
	if (*(int*)fileBegin == 0x5A4D) {
		printf("OK, FOUND MZ\n");
		
		fileBegin2 = fileBegin;
		
		if (*(int*)((char*)fileBegin2 + 0x3C) < fileSize) {
			printf("OK, OFFSET SMALLER THAN FILESIZE\n");
			
			offset = *(int*)((char*)fileBegin2 + 0x3C);
			PE = (int*)((char*)fileBegin2 + offset);
			if (*PE == 0x4550) {
				printf("OK, FOUND PE\n");
				
				test1 = *(int*)((char*)fileBegin2 + offset + 4) == 0x14C;
				test2 = (*(int*)((char*)fileBegin2 + offset + 22) & 2);
				
				if (test1 && test2) {
					printf("OK, FOUND 0x14C, PASSED &2\n");
					
					//printf("[%x]", *(int*)((char*)fileBegin2 + offset + 8));
				
					if ( *(int*)((char*)fileBegin2 + offset + 8) == 0x57D1B2A2) {
						printf("bin1\n");
					}
					else if (*(int*)((char*)fileBegin2 + offset + 8) == 0x57D2B0F8) {
						printf("bin2\n");
					}
					else if (*(int*)((char*)fileBegin2 + offset + 8) == 0x49180192) {
						printf("bin3\n");
					}
					else if (*(int*)((char*)fileBegin2 + offset + 8) == 0x579E9100) {
						printf("bin4\n");
					}
				}
			}
		}
	}
	

	return 0;
}