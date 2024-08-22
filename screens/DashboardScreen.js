import React, { useState } from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { Calendar } from 'react-native-calendars';

const notes = {
  '2024-08-10': 'Meeting with team',
  '2024-08-12': 'Doctor appointment',
};

const todos = {
  '2024-08-10': ['Finish project report', 'Call the client'],
  '2024-08-12': ['Buy groceries'],
};

export default function DashboardScreen() {
  const [selectedDate, setSelectedDate] = useState('');

  const handleDayPress = (day) => {
    setSelectedDate(day.dateString);
  };

  return (
    <View style={styles.container}>
      <Calendar
        onDayPress={handleDayPress}
        markedDates={{
          [selectedDate]: { selected: true, marked: true, selectedColor: 'blue' }
        }}
      />
      <ScrollView style={styles.detailsContainer}>
        <Text style={styles.dateText}>Selected Date: {selectedDate}</Text>
        <Text style={styles.sectionTitle}>Notes:</Text>
        <Text>{notes[selectedDate] || 'No notes for this day'}</Text>
        <Text style={styles.sectionTitle}>To-Do List:</Text>
        <View>
          {(todos[selectedDate] || []).length === 0 ? (
            <Text>No to-dos for this day</Text>
          ) : (
            todos[selectedDate].map((todo, index) => (
              <Text key={index}>- {todo}</Text>
            ))
          )}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  detailsContainer: {
    flex: 1,
    marginTop: 20,
  },
  dateText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 10,
  },
});
