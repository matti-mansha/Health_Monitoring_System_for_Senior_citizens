import * as React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import Login from './src/screens/Login';
import HomeScreen from './src/screens/HomeScreen';
import Display from './src/screens/Display';
const Stack = createNativeStackNavigator();

const App = () => {
  return (
    //<ModelNotification/>
     <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          
       />
       <Stack.Screen name="Login" component={Login} />
      <Stack.Screen name="Display" component={Display} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};
export default App;