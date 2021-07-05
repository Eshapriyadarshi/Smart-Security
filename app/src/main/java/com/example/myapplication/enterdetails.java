package com.example.myapplication;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;

public class enterdetails extends AppCompatActivity {
    EditText mphone1, mphone2, mphone3, msecu;
    Button mSave;
    private FirebaseFirestore mFirebase;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_enterdetails);

        mphone1 = findViewById(R.id.editTextPhone);
        mphone2 = findViewById(R.id.editTextPhone2);
        mphone3 = findViewById(R.id.editTextPhone3);
        msecu = findViewById(R.id.sec);
        mSave = findViewById(R.id.button4);

        mFirebase = FirebaseFirestore.getInstance();
        mSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String phone1 = mphone1.getText().toString();
                String phone2 = mphone2.getText().toString();
                String phone3 = mphone3.getText().toString();
                String security = msecu.getText().toString();
                String n = "0";

                savetofirestore(security,phone1,phone2,phone3,n);
            }
        });
    }

    private void savetofirestore(String security, String phone1, String phone2, String phone3, String n) {
        if(!phone1.isEmpty() && !phone2.isEmpty()){
            HashMap<String , Object> map = new HashMap<>();
            map.put("phone1",phone1);
            map.put("phone2",phone2);
            map.put("phone3",phone3);
            map.put("security",security);
            map.put("n",n);

            mFirebase.collection("USERS").document(security).set(map)
                    .addOnCompleteListener(new OnCompleteListener<Void>() {
                        @Override
                        public void onComplete(@NonNull Task<Void> task) {
                            if (task.isSuccessful()){
                                Toast.makeText(enterdetails.this, "SAVED", Toast.LENGTH_SHORT).show();
                            }
                        }
                    }).addOnFailureListener(new OnFailureListener() {
                @Override
                public void onFailure(@NonNull Exception e) {
                    Toast.makeText(enterdetails.this, "FAILED", Toast.LENGTH_SHORT).show();
                }
            });


        }

    }
}