import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { HomeScreen } from './src/screens/HomeScreen';
import { BreakScreen } from './src/screens/BreakScreen';
import { HotelsScreen } from './src/screens/HotelsScreen';
import { SOSScreen } from './src/screens/SOSScreen';
import { ReviewScreen } from './src/screens/ReviewScreen';
import { DashboardScreen } from './src/screens/DashboardScreen';

const Stack = createNativeStackNavigator();

function App(): React.JSX.Element {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'Travel Buddy' }} />
        <Stack.Screen name="Breaks" component={BreakScreen} />
        <Stack.Screen name="Hotels" component={HotelsScreen} />
        <Stack.Screen name="SOS" component={SOSScreen} options={{ headerStyle: { backgroundColor: '#ffebee' }, headerTintColor: 'red' }} />
        <Stack.Screen name="Review" component={ReviewScreen} />
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;
