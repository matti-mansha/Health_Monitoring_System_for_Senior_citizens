import React, { useState } from 'react';
import { View,TouchableOpacity, TextInput, Button,Text, Alert, StyleSheet } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import {ImageBackground} from 'react-native';
import { Image } from 'react-native';


const HomeScreen = ({navigation}) => {
 
  
   

  return(
    <View>
    <ImageBackground source={require('../screens/assets/leaves1.jpg')}>

    <View style={styles.abc}>
      <Text style={styles.mainHeader}>
      Health Monitoring System For Senior Citizen </Text> 
      <Text>{'\n'} </Text>
      <View style={styles.imageContainer}>
      <Image source={require('../screens/assets/workflow.jpg')} style={styles.image} />
</View>
   
     

<View>
<Text>{'\n'} </Text>
    <TouchableOpacity style={[
      styles.buttonStyle,
      {
        backgroundColor : 'blue' ,
      },
    ]}
>
<Text style={styles.buttonText} onPress={() => navigation.navigate('Login')}>
    
  Go to Login
</Text>
     
    </TouchableOpacity>
   
    </View>
    </View>
    </ImageBackground>

</View>
    );
};

const styles=StyleSheet.create({
    abc:{
        height:"100%",
        paddingHorizontal: 30,
        paddingTop:50,
        

       // backgroundColor:"yellow"
       // justifyContent: 'center',
       color: 'black',
       fontSize: 42,
       lineHeight: 84,
       fontWeight: 'bold',
       textAlign: 'center',
      
        
    },
    imageContainer: {
        alignItems: 'center',
      },
    image: {
        width: 200,
        height: 200,
        justifyContent: 'center',
    
      },
    mainHeader:{
        fontSize:25,color: "black",
        fontWeight:"500",
        paddingTop:0,
        paddingBottom:0,
    
        
    },
    ccc: {
    fontSize: 25,
    fontWeight:"600",
    color: 'black',
    paddingBottom: 20,
    lineHeight: 25,
    

  },
  inputContainer: {
    marginTop: 0,
  },
labels: {
    fontSize: 18,
    color: 'black',
    marginTop: 10,
    marginBottom: 5,
    lineHeight: 25,
    
  },
  inputStyle: {
    borderWidth: 1,
    borderColor: 'rgba(0,0,0,0.3)',
    paddingHorizontal: 15,
    paddingVertical: 7,
    borderRadius: 1,
    
    fontSize: 18,
  },
wrapper: {
    // paddingHorizontal: 10,
    // paddingVertical: 15,
    // paddingBottom: 30
    flexDirection:"row",
    // justifyContent:'center',
    alignItems:"center",
    marginTop: 15,
    marginBottom: 360
    // alignContent:"center"

  },
  wrapperText: {
    // paddingLeft: 30
    marginTop: 0,
  },
buttonStyle: {
    borderRadius: 40,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center'

  },
  buttonText: {
    color: '#fff',
    fontSize: 20,
    justifyContent: 'center',
    alignContent: 'center',
    fontWeight: '600'
  },
});
export default HomeScreen;
