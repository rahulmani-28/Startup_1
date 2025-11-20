import React, { useCallback, useRef, useState } from 'react';
import {
    SafeAreaView,
    ScrollView,
    StatusBar,
    StyleSheet,
    Text,
    useColorScheme,
    View,
    Button,
} from 'react-native';
import { Colors } from 'react-native/Libraries/NewAppScreen';
import Geolocation from '@react-native-community/geolocation';
import { api } from '../api/client';

function Section({ children, title }: any) {
    const isDarkMode = useColorScheme() === 'dark';
    return (
        <View style={styles.sectionContainer}>
            <Text style={[styles.sectionTitle, { color: isDarkMode ? Colors.white : Colors.black }]}>
                {title}
            </Text>
            <Text style={[styles.sectionDescription, { color: isDarkMode ? Colors.light : Colors.dark }]}>
                {children}
            </Text>
        </View>
    );
}

export function HomeScreen({ navigation }: any) {
    const isDarkMode = useColorScheme() === 'dark';
    const backgroundStyle = { backgroundColor: isDarkMode ? Colors.darker : Colors.lighter };

    const [journeyId, setJourneyId] = useState<string | null>(null);
    const [speed, setSpeed] = useState<number>(0);
    const [distanceKm, setDistanceKm] = useState<number>(0);
    const [eta, setEta] = useState<string | null>(null);

    const journeyIdRef = useRef<string | null>(null);
    const distanceKmRef = useRef<number>(0);
    const lastPos = useRef<{ lat: number; lon: number } | null>(null);
    const watchId = useRef<number | null>(null);
    const startTimeRef = useRef<number>(0);

    const toRad = (v: number) => (v * Math.PI) / 180;
    const haversineKm = (a: { lat: number; lon: number }, b: { lat: number; lon: number }) => {
        const R = 6371;
        const dLat = toRad(b.lat - a.lat);
        const dLon = toRad(b.lon - a.lon);
        const lat1 = toRad(a.lat);
        const lat2 = toRad(b.lat);
        const x =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x));
        return R * c;
    };

    const start = useCallback(async () => {
        try {
            Geolocation.getCurrentPosition(async pos => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const res = await api.startJourney({
                    user_id: 'demo-user',
                    start_location: { lat, lon },
                    destination: { lat, lon },
                    total_distance_km: 300,
                });
                setJourneyId(res.journey_id);
                journeyIdRef.current = res.journey_id;

                setDistanceKm(0);
                distanceKmRef.current = 0;
                startTimeRef.current = Date.now();

                watchId.current = Geolocation.watchPosition(async p => {
                    const cur = { lat: p.coords.latitude, lon: p.coords.longitude };
                    if (lastPos.current) {
                        const delta = haversineKm(lastPos.current, cur);
                        distanceKmRef.current += delta;
                        setDistanceKm(distanceKmRef.current);
                    }
                    lastPos.current = cur;
                    const kmph = Math.max(0, (p.coords.speed ?? 0) * 3.6);
                    setSpeed(kmph);

                    if (journeyIdRef.current) {
                        const track = await api.trackJourney({
                            journey_id: journeyIdRef.current,
                            telemetry: {
                                location: cur,
                                speed_kmph: kmph,
                                distance_covered_km: distanceKmRef.current,
                            },
                        });
                        setEta(track.eta_iso ?? null);
                    }
                }, err => console.warn(err), { enableHighAccuracy: true, distanceFilter: 5 });
            }, err => console.warn(err), { enableHighAccuracy: true });
        } catch (e) {
            console.warn('start error', e);
        }
    }, []);

    const stop = useCallback(async () => {
        try {
            if (watchId.current != null) {
                Geolocation.clearWatch(watchId.current);
                watchId.current = null;
            }
            if (journeyId) {
                await api.stopJourney({ journey_id: journeyId });
            }
            setJourneyId(null);
            journeyIdRef.current = null;
            setEta(null);
        } catch (e) {
            console.warn('stop error', e);
        }
    }, [journeyId]);

    return (
        <SafeAreaView style={backgroundStyle}>
            <StatusBar barStyle={isDarkMode ? 'light-content' : 'dark-content'} backgroundColor={backgroundStyle.backgroundColor} />
            <ScrollView contentInsetAdjustmentBehavior="automatic" style={backgroundStyle}>
                <View style={{ backgroundColor: isDarkMode ? Colors.black : Colors.white, padding: 20 }}>
                    <Section title="Journey Tracker">
                        <Text style={styles.highlight}>Speed:</Text> {speed.toFixed(1)} km/h{'\n'}
                        <Text style={styles.highlight}>Distance:</Text> {distanceKm.toFixed(2)} km{'\n'}
                        <Text style={styles.highlight}>ETA:</Text> {eta ?? '-'}{'\n'}
                    </Section>

                    <View style={{ flexDirection: 'row', gap: 12, marginVertical: 20 }}>
                        <Button title="Start" onPress={start} disabled={!!journeyId} />
                        <Button title="Stop" onPress={stop} disabled={!journeyId} />
                    </View>

                    <View style={styles.menuGrid}>
                        <Button title="Breaks" onPress={() => navigation.navigate('Breaks', {
                            journeyId,
                            totalDistance: distanceKm,
                            elapsedTime: (Date.now() - startTimeRef.current) / 3600000
                        })} />
                        <Button title="Hotels" onPress={() => navigation.navigate('Hotels')} />
                        <Button title="SOS" color="red" onPress={() => navigation.navigate('SOS', { journeyId })} />
                        <Button title="Dashboard" onPress={() => navigation.navigate('Dashboard')} />
                    </View>
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    sectionContainer: { marginTop: 32, paddingHorizontal: 24 },
    sectionTitle: { fontSize: 24, fontWeight: '600' },
    sectionDescription: { marginTop: 8, fontSize: 18, fontWeight: '400' },
    highlight: { fontWeight: '700' },
    menuGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 20, justifyContent: 'center' }
});
