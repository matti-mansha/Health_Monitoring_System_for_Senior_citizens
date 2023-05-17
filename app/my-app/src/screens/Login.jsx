import React, { useState } from 'react';
import { View,TouchableOpacity, TextInput, Button,Text, Alert, StyleSheet } from 'react-native';
import {ImageBackground} from 'react-native';
import Display from './Display';
const Login = ({navigation}) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
   const handleLogin = async () => {
    try {
      const response = await fetch("http://192.168.137.213:5000/login", {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        // Successful login
        // Redirect or do something else
      // Alert.alert('Login successful');
      // <Display /> 
      navigation.navigate('Display');
       console.log('Login successful');
    //navigation.navigate('HomeScreen');

      } else {
        // Invalid credentials or server error
       // const errorData = await response.json();
       // const errorMessage = errorData.message || 'Invalid credentials';
        Alert.alert('Invalid Username or Password');
      }
    } catch (error) {
      console.error('Error occurred during login:', error);
      Alert.alert('Login failed', 'An error occurred during login');
    }
  };

  return(
    <View>
    <ImageBackground source={require('../screens/assets/leaves1.jpg')}>
    <View style={styles.abc}>
      <Text style={styles.mainHeader}>
      Health Monitoring System For Senior Citizen </Text> 
      <Text>{'\n'} </Text>
      <Text style={styles.ccc}>
        Login Form
      </Text>
   
      <TextInput
        style={styles.inputStyle}
        placeholder="Email"
        value={email}
        onChangeText={text => setEmail(text)}
      />
      <Text>{'\n'} </Text>
      <TextInput
        style={styles.inputStyle}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={text => setPassword(text)}
      />

<View>
<Text>{'\n'} </Text>
    <TouchableOpacity style={[
      styles.buttonStyle,
      {
        backgroundColor : 'blue' ,
      },
    ]}
>
      <Text style={styles.buttonText} onPress={handleLogin} >Login</Text>
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
export default Login;
