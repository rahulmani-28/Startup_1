import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { api } from '../api/client';

export function ReviewScreen({ route, navigation }: any) {
    const { hotelId, hotelName } = route.params || {};
    const [rating, setRating] = useState('');
    const [comment, setComment] = useState('');

    const submit = async () => {
        try {
            await api.submitReview({
                hotel_id: hotelId,
                user_id: "demo-user",
                rating: parseInt(rating),
                comment,
                tags: ["clean"] // Mock tags
            });
            Alert.alert("Success", "Review submitted!");
            navigation.goBack();
        } catch (e) {
            Alert.alert("Error", "Failed to submit review");
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Review {hotelName}</Text>

            <TextInput
                placeholder="Rating (1-5)"
                keyboardType="numeric"
                style={styles.input}
                value={rating}
                onChangeText={setRating}
            />

            <TextInput
                placeholder="Write your review..."
                multiline
                style={[styles.input, { height: 100 }]}
                value={comment}
                onChangeText={setComment}
            />

            <Button title="Submit Review" onPress={submit} />
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
    input: { borderWidth: 1, borderColor: '#ccc', padding: 10, borderRadius: 5, marginBottom: 15, fontSize: 16 },
});
