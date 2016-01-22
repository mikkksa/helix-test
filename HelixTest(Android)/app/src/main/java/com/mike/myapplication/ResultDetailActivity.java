package com.mike.myapplication;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.drawable.ClipDrawable;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.LayerDrawable;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Adapter;
import android.widget.ArrayAdapter;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import android.widget.SimpleAdapter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class ResultDetailActivity extends Activity {
    ListView listView;
    GlobalIP globalIP;
    RelativeLayout content;

    // имена атрибутов для Map
    final String ATTRIBUTE_NAME_TEXT = "text";
    final String ATTRIBUTE_NAME_PB = "pb";
    final String ATTRIBUTE_NAME_LL = "ll";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        LayoutInflater inflater = getLayoutInflater();
        content = (RelativeLayout) inflater.inflate(R.layout.activity_result_detail, null);
        setContentView(content);

        List<Double> load = new ArrayList<>();
        listView = (ListView)findViewById(R.id.listView3);
        globalIP = (GlobalIP)this.getApplication();
        List<InterviewResult> results = globalIP.getResults();
        List<String> names = new ArrayList<>();
        int allchoices = 0;

        for(int i =0; i < results.size(); i++){
            allchoices += Integer.parseInt(results.get(i).pick);
        }

        for(int i = 0; i < results.size(); i++){
            Double piece = (double)Integer.parseInt(results.get(i).pick)*100/allchoices;
            piece *= 1000;
            int d = (int)Math.round(piece);
            piece = (double)d/1000;
            load.add(piece);
            names.add(results.get(i).choice + "\t" + String.valueOf(piece) + "%");
        }

        // упаковываем данные в понятную для адаптера структуру
        ArrayList<Map<String, Object>> data = new ArrayList<>(
                load.size());
        Map<String, Object> m;

        for (int i = 0; i < load.size(); i++) {
            m = new HashMap<>();
            m.put(ATTRIBUTE_NAME_TEXT, results.get(i).choice + ". Progress: " + load.get(i) + "%");
            m.put(ATTRIBUTE_NAME_PB, load.get(i));
            m.put(ATTRIBUTE_NAME_LL, load.get(i));
            data.add(m);
        }
        // массив имен атрибутов, из которых будут читаться данные
        String[] from = { ATTRIBUTE_NAME_TEXT, ATTRIBUTE_NAME_PB,
                ATTRIBUTE_NAME_LL };
        // массив ID View-компонентов, в которые будут вставлять данные
        int[] to = { R.id.tvLoad, R.id.pbLoad, R.id.llLoad };
        SimpleAdapter simpleAdapter = new SimpleAdapter(this, data, R.layout.int_result_item, from, to);
        simpleAdapter.setViewBinder(new MyViewBinder());
        ArrayAdapter adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, names);
        listView.setAdapter(simpleAdapter);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}

class MyViewBinder implements SimpleAdapter.ViewBinder {


    @Override
    public boolean setViewValue(View view, Object data,
                                String textRepresentation) {
        int i = 0;
        switch (view.getId()) {
            // LinearLayout
            case R.id.llLoad:
                i = ((Double) data).intValue();
                if (i < 200) view.setBackgroundColor(Color.GREEN); else
                if (i < 150) view.setBackgroundColor(Color.YELLOW); else
                    view.setBackgroundColor(Color.RED);
                return true;
            // ProgressBar
            case R.id.pbLoad:
                i = ((Double) data).intValue();
                ((ProgressBar)view).setProgress(i);
                return true;
        }
        return false;
    }
}


