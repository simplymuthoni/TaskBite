import React from 'react';
import { StyleSheet, Text, View, Image, Dimensions, TouchableOpacity } from 'react-native';
import Carousel from 'react-native-snap-carousel';

const { width: screenWidth } = Dimensions.get('window');

const slides = [
  {
    title: 'Get Your notes in order',
    description: 'Write down important items, move around with ease.',
    image: require('../assets/s1.png'),
  },
  {
    title: 'Keep up with your to do list',
    description: 'Add reminders, and allocate priority status.',
    image: require('../assets/s2.png'),
  },
  {
    title: 'TaskBite',
    description: 'Your one and stop journal.',
    image: require('../assets/s3.png'),
  },
];

export default function OnboardingScreen({ navigation: { replace } }) {
  const renderSlide = ({ item }) => (
    <View style={styles.slide}>
      <Image source={item.image} style={styles.image} />
      <Text style={styles.title}>{item.title}</Text>
      <Text style={styles.description}>{item.description}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Carousel
        data={slides}
        renderItem={renderSlide}
        sliderWidth={screenWidth}
        itemWidth={screenWidth}
        loop
      />
      <TouchableOpacity style={styles.getStartedButton} onPress={() => replace('Auth')}>
        <Text style={styles.getStartedText}>Get Started</Text>
      </TouchableOpacity>
      <Text style={styles.skip} onPress={() => replace('Auth')}>
        Skip
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  slide: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: screenWidth * 0.8,
    height: screenWidth * 1.2,
    resizeMode: 'contain',
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
  },
  description: {
    fontSize: 16,
    textAlign: 'center',
    color: '#777',
  },
  getStartedButton: {
    backgroundColor: '#007BFF',
    borderRadius: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    marginTop: 20,
  },
  getStartedText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  skip: {
    fontSize: 18,
    color: '#007BFF',
    padding: 20,
    textAlign: 'center',
  },
});
