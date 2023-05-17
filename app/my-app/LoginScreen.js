import React, { useState } from 'react';
import { View,TouchableOpacity, Text,TextInput, Button, Alert, StyleSheet } from 'react-native';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await fetch("http://localhost:3000/login", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        // Successful login
        // Redirect or do something else
        Alert.alert('Login successful');
        console.log("success")
      } else {
        // Invalid credentials or server error
        const errorData = await response.json();
        const errorMessage = errorData.message || 'Invalid credentials';
        Alert.alert('Login failed', errorMessage);
        console.log("error")
      }
    } catch (error) {
      console.error('Error occurred during login:', error);
      Alert.alert('Login failed', 'An error occurred during login');
    }
  };

  return (
    <View style={styles.container}>
      <Text>{'\n'} </Text>
      <Text>{'\n'} </Text>
      <Text>{'\n'} </Text>
      <Text>{'\n'} </Text>
      
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={text => setEmail(text)}
      />
      <TextInput
        style={styles.input}
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
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  input: {
    width: '100%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 16,
    paddingHorizontal: 8,
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





<View style={styles.inputContainer}>
<Text style={styles.labels}>Enter your email</Text>
<TextInput 
style={styles.inputStyle}
autoCapitalize="none"
autoCorrect={false}
/>
</View>
<View style={styles.inputContainer}>
<Text style={styles.labels}> Enter your password </Text>

<TextInput 
style={styles.inputStyle}
autoCapitalize="none"
autoCorrect={false}
secureTextEntry={true}
/>
</View>