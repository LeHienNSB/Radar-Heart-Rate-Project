#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
#include<vector>
#include<stdio.h>
#include<cstring>
using namespace std;

#define HEART_RATE_TYPE 0
#define RESPIRATORY_TYPE 1
#define DISTANCE_TYPE 2
#define BODY_TYPE 3
#define AVERAGE_ELEMENT_NUM 15

typedef struct 
{
    int buff[AVERAGE_ELEMENT_NUM];
    int head;
    int tail;
} ringBuffer;


int main(){
    fstream excel;
    ofstream avrData;
    excel.open("A_1_5.csv");
    avrData.open("Averageres15.csv");

    ringBuffer senHRBuff;
    ringBuffer realHRBuff;
    string lineEx;
    int tempIndex=0;
    senHRBuff.head=0;
    senHRBuff.tail=0;

    realHRBuff.head=0;
    realHRBuff.tail=0;
    
    memset(senHRBuff.buff, 0, sizeof(senHRBuff.buff));
    memset(realHRBuff.buff, 0, sizeof(realHRBuff.buff));
    while (getline(excel, lineEx))
    {
        if(lineEx[0]=='\t'){
            stringstream ss(lineEx);
            string tempString;
            vector<string> tempVector;
            int average=0, averageReal=0;

            while (getline(ss, tempString, ','))
            {
                tempVector.push_back(tempString);
            }
            
            // if(tempVector[1]=="0" || tempVector.size()<9){
            //     continue;
            // }
            tempIndex++;
            senHRBuff.buff[senHRBuff.tail]=stoi(tempVector[2].substr(1,tempVector[2].length()-1));
            senHRBuff.tail=(senHRBuff.tail+1)%AVERAGE_ELEMENT_NUM;

            // realHRBuff.buff[realHRBuff.tail]=stoi(tempVector[8]);
            // realHRBuff.tail=(realHRBuff.tail+1)%AVERAGE_ELEMENT_NUM;

            for(int i=0;i<AVERAGE_ELEMENT_NUM;i++){
                average+=senHRBuff.buff[i];
                // averageReal+=realHRBuff.buff[i];
            }
            average=(tempIndex<AVERAGE_ELEMENT_NUM)?(average/tempIndex):(average/AVERAGE_ELEMENT_NUM);
            // averageReal=(tempIndex<AVERAGE_ELEMENT_NUM)?(averageReal/tempIndex):(averageReal/AVERAGE_ELEMENT_NUM);
            // cout<<lineEx.substr(0,9)<<average<<","<<averageReal<<'\n';
            avrData<<lineEx<<","<<average<<'\n';
        }
        else{
            avrData<<'\n';
        }
        

    }
    
    excel.close();
    avrData.close();
}