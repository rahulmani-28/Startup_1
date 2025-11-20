import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet, Alert } from 'react-native';
import { api } from '../api/client';

export function BreakScreen({ route, navigation }: any) {
    const { journeyId, totalDistance, elapsedTime } = route.params || {};
    const [suggestion, setSuggestion] = useState<string | null>(null);
    const [timer, setTimer] = useState(0);
    const [isTimerRunning, setIsTimerRunning] = useState(false);

    useEffect(() => {
        if (journeyId) {
            api.suggestBreak({
                journey_id: journeyId,
                total_distance_km: totalDistance || 0,
                elapsed_time_hours: elapsedTime || 0,
            }).then(res => {
                if (res.should_take_break) {
                    setSuggestion(res.reason || "Time for a break!");
                }
            }).catch(console.warn);
        }
    }, [journeyId]);

    useEffect(() => {
        let interval: any;
        if (isTimerRunning) {
            interval = setInterval(() => {
                setTimer(t => t + 1);
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [isTimerRunning]);

    const formatTime = (s: number) => {
        const m = Math.floor(s / 60);
        const sec = s % 60;
        return `${m}:${sec < 10 ? '0' : ''}${sec}`;
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Break Management</Text>

            {suggestion && (
                <View style={styles.suggestionBox}>
                    <Text style={styles.suggestionText}>⚠️ Suggestion: {suggestion}</Text>
                    <Button title="Find Nearby Hotels" onPress={() => navigation.navigate('Hotels')} />
                </View>
            )}

            <View style={styles.timerBox}>
                <Text style={styles.timerText}>{formatTime(timer)}</Text>
                <View style={styles.controls}>
                    <Button title={isTimerRunning ? "Pause" : "Start Timer"} onPress={() => setIsTimerRunning(!isTimerRunning)} />
                    <Button title="Reset" onPress={() => { setIsTimerRunning(false); setTimer(0); }} />
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20, alignItems: 'center' },
    title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
    suggestionBox: { backgroundColor: '#ffebee', padding: 15, borderRadius: 10, marginBottom: 20, width: '100%' },
    suggestionText: { fontSize: 16, color: '#c62828', marginBottom: 10 },
    timerBox: { alignItems: 'center', marginTop: 20 },
    timerText: { fontSize: 48, fontWeight: 'bold', marginBottom: 20 },
    controls: { flexDirection: 'row', gap: 20 },
});
