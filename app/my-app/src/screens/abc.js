import { StatusBar } from 'expo-status-bar';
import { StyleSheet, ImageBackground,Text, View } from 'react-native';
import Login from './src/screens/Login';
import HomeScreen from './src/screens/HomeScreen';
const RootStack = createStackNavigator(
  {
    Login: Login,
    
  },
  {
    initialRouteName: "Login"
  }
);
const App = () =>{
  return (
  <View>
        <ImageBackground source={require('./assets/leaves1.jpg')}>
  
       <HomeScreen/>
       </ImageBackground>

  </View>
)};
export default App;