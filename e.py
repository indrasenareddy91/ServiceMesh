[08/04, 8:37 am] G.Vineeth: // CLIENT
#include <iostream>
#include <thread>
#include <arpa/inet.h>
#include <unistd.h>
using namespace std;

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in server{};
    server.sin_family = AF_INET;
    server.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &server.sin_addr);

    connect(sock, (sockaddr*)&server, sizeof(server));

    // receive thread
    thread t([&]() {
        char buffer[1024];
        while (true) {
            int n = read(sock, buffer, sizeof(buffer));
            if (n > 0) {
                cout << "\nMessage: " << string(buffer, n) << endl;
            }
        }
    });

    // send messages
    while (true) {
        string msg;
        getline(cin, msg);

        write(sock, msg.c_str(), msg.size());
    }
}
[08/04, 8:37 am] G.Vineeth: #include <iostream>
#include <thread>
#include <vector>
#include <arpa/inet.h>
#include <unistd.h>
using namespace std;

vector<int> clients;

void handleclient(int sock){
    char buffer[1024];
    
    while(true){
        int n = read(sock, buffer, sizeof(buffer));
        if (n <= 0) break;
        
        for(int c : clients){
            if(c!=sock){
                write(c,buffer,n);
            }
        }
    }
    
    close(sock);
}

int main(){
    int server = socket(AF_INET,SOCK_STREAM,0);
    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8080);
    addr.sin_addr.s_addr = INADDR_ANY;
    
    bind(server, (sockaddr*)&addr, sizeof(addr));
    listen(server, 5);
    
    cout << "Server started : ";
    while(true){
        int client = accept(server, NULL, NULL);
        clients.push_back(client);
        
        thread(handleclient, client).detach();
    }
}
