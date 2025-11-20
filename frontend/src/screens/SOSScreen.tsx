import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import Geolocation from '@react-native-community/geolocation';
import { api } from '../api/client';

export function SOSScreen({ route }: any) {
    const { journeyId } = route.params || {};
    const [alertSent, setAlertSent] = useState(false);

    const handleSOS = () => {
        Geolocation.getCurrentPosition(async pos => {
            try {
                await api.triggerSOS({
                    journey_id: journeyId || "unknown",
                    location: { lat: pos.coords.latitude, lon: pos.coords.longitude },
                    type: "manual"
                });
                setAlertSent(true);
                Alert.alert("SOS Sent", "Emergency contacts and nearest stations have been notified.");
            } catch (e) {
                Alert.alert("Error", "Failed to send SOS");
            }
        });
    };

    return (
        <View style={styles.container}>
            <TouchableOpacity style={styles.sosButton} onPress={handleSOS}>
                <Text style={styles.sosText}>SOS</Text>
            </TouchableOpacity>
            <Text style={styles.helpText}>Press for Emergency Help</Text>

            {alertSent && (
                <View style={styles.statusBox}>
                    <Text style={styles.statusText}>✅ Help is on the way!</Text>
                    <Text>Notified: Police, Hospital, Family</Text>
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#ffebee' },
    sosButton: {
        width: 200, height: 200, borderRadius: 100, backgroundColor: 'red',
        justifyContent: 'center', alignItems: 'center', elevation: 10,
        shadowColor: 'red', shadowOpacity: 0.5, shadowRadius: 20
    },
    sosText: { color: 'white', fontSize: 48, fontWeight: 'bold' },
    helpText: { marginTop: 20, fontSize: 18, color: '#555' },
    statusBox: { marginTop: 40, padding: 20, backgroundColor: 'white', borderRadius: 10, alignItems: 'center' },
    statusText: { fontSize: 20, fontWeight: 'bold', color: 'green', marginBottom: 5 },
});
