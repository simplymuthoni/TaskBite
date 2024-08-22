import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from './screens/HomeScreen.js';
import AuthScreen from './screens/AuthScreen';
import LoginScreen from './screens/LoginScreen.js';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Auth" component={AuthScreen} />
        <Stack.Screen name="Login" component={LoginScreen}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
}
