package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    Button mbutton1,mbutton2,mbutton3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mbutton1 = findViewById(R.id.button);
        mbutton2 = findViewById(R.id.button2);
        mbutton3 = findViewById(R.id.button3);

        mbutton1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this,enterdetails.class));
            }
        });
        mbutton3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SharedPreferences logs = getSharedPreferences("checkbox",MODE_PRIVATE);
                SharedPreferences.Editor editor = logs.edit();
                editor.putString("remember","false");
                editor.apply();
                startActivity(new Intent(MainActivity.this,login.class));
                finish();
            }
        });

    }

}