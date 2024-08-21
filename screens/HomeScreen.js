import React from 'react';
import { StyleSheet, Text, View, Image } from 'react-native';
import { Button } from 'galio-framework';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Image source={require('../assets/logo.png')} style={styles.iconContainer} />
      <Text h1>Welcome to <Text bold>TaskBite</Text></Text>
      <Button
        round
        uppercase
        color="success"
        onPress={() => navigation.navigate('Auth')}
      >
        Get Started
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  iconContainer: {
    width: 300,
    height: 200,
    marginBottom: 20,
  },
});
