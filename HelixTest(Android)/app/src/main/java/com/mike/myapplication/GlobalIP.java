package com.mike.myapplication;

import android.app.Application;

import java.util.List;

public class GlobalIP extends Application {
    private static GlobalIP globalIP;
    public static String ip;
    public static String userid;
    public List<Interview> interviews;
    public List<Choice> choices;
    public List<InterviewResult> results;

    public GlobalIP getInstance(){
        return globalIP;
    }
    public String getIp(){
        return ip;
    }
    public String getUserid(){
        return userid;
    }
    public List<Choice> getChoices(){
        return choices;
    }
    public List<Interview> getInterviews(){
        return interviews;
    }
    public List<InterviewResult> getResults(){
        return results;
    }

    public void setip(String ip_){
        ip = ip_;
    }
    public void setUserid(String userid_){
        userid = userid_;
    }
    public void setInterviews(List<Interview> interviews1){
        interviews = interviews1;
    }
    public void setChoices(List<Choice> choices1){
        choices = choices1;
    }
    public void setResults(List<InterviewResult> results1){
        results = results1;
    }

    @Override
    public void onCreate(){
        super.onCreate();
        globalIP = this;
        userid = "4";
        ip = "http://192.168.1.4:8000";
    }
}
