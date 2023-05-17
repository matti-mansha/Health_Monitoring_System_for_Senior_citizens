import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Alert } from 'react-native';
import axios from 'axios';

const Display = () => {
const [message, setMessage] = useState('');

useEffect(() => {
const intervalId = setInterval(() => {
axios
.get('http://192.168.137.213:3000/api/message')
.then((response) => {
const newMessage = response.data.message;
if (newMessage !== '') {
  if (message === '') {
    setMessage(newMessage);
    showNotification('New Message', newMessage);
  }
} else {
  setMessage('');
}
})
.catch((error) => {
console.error(error);
});
}, 1000);

return () => {
clearInterval(intervalId);
};
}, []);

const showNotification = (title, message) => {
Alert.alert(title, message, [
{
text: 'OK',
onPress: () => {
setMessage('');
},
},
]);
};

const patientStatus = message === '' ? 'Normal' : 'Abnormal';

return (
<View style={styles.container}>
<Text style={styles.message}>Patient Status: {patientStatus}</Text>
</View>
);
};

const styles = StyleSheet.create({
  container: {
  flex: 1,
  justifyContent: 'flex-start',
  alignItems: 'center',
  paddingVertical: 100, // Adjust the padding as needed
  backgroundColor: '#f5f5f5',
  },
  patientStatus: {
  fontSize: 24,
  fontWeight: 'bold',
  textAlign: 'center',
  marginHorizontal: 50,
  marginBottom: 50,
  color: '#333',
  },
  message: {
  fontSize: 24,
  fontWeight: 'bold',
  textAlign: 'center',
  marginHorizontal: 20,
  color: '#333',
  },
  });
  export default Display;