import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, Button, ActivityIndicator } from 'react-native';
import Geolocation from '@react-native-community/geolocation';
import { api } from '../api/client';

export function HotelsScreen({ navigation }: any) {
    const [hotels, setHotels] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setLoading(true);
        Geolocation.getCurrentPosition(async pos => {
            try {
                const res = await api.searchHotels({
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude,
                    radius_km: 5
                });
                setHotels(res.hotels);
            } catch (e) {
                console.warn(e);
            } finally {
                setLoading(false);
            }
        }, err => {
            console.warn(err);
            setLoading(false);
        });
    }, []);

    const renderItem = ({ item }: any) => (
        <View style={styles.card}>
            <Text style={styles.hotelName}>{item.name}</Text>
            <Text>Rating: {item.rating} ⭐</Text>
            <View style={styles.tags}>
                {item.tags.map((t: string) => (
                    <Text key={t} style={styles.tag}>{t}</Text>
                ))}
            </View>
            <Button title="Write Review" onPress={() => navigation.navigate('Review', { hotelId: item.id, hotelName: item.name })} />
        </View>
    );

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Nearby Hotels</Text>
            {loading ? <ActivityIndicator size="large" /> : (
                <FlatList
                    data={hotels}
                    renderItem={renderItem}
                    keyExtractor={item => item.id}
                    contentContainerStyle={{ paddingBottom: 20 }}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 10 },
    title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
    card: { backgroundColor: 'white', padding: 15, borderRadius: 10, marginBottom: 10, elevation: 2 },
    hotelName: { fontSize: 18, fontWeight: 'bold' },
    tags: { flexDirection: 'row', gap: 5, marginVertical: 5 },
    tag: { backgroundColor: '#e0e0e0', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 5, fontSize: 12 },
});
