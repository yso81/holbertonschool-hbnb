
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, Image, TouchableOpacity, ActivityIndicator, RefreshControl, StyleSheet, Dimensions } from 'react-native';

const API_BASE_URL = 'https://keyless-subdistichously-mavis.ngrok-free.dev/api/v1';
const { width } = Dimensions.get('window');

export default function PlacesListScreen() {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const fetchPlaces = async () => {
    try {
      setError(null);
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);
      
      const response = await fetch(`${API_BASE_URL}/places/`, {
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setPlaces(data);
      setLoading(false);
      setRefreshing(false);
    } catch (err) {
      if (err.name === 'AbortError') {
        setError('Request timeout - server took too long to respond');
      } else {
        setError(err.message || 'Unknown error occurred');
      }
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchPlaces();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchPlaces();
  };

  const getPlaceholderImage = (index) => {
    const images = [
      'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800',
      'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800',
      'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800',
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',
      'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
    ];
    return images[index % images.length];
  };

  const renderPlace = ({ item, index }) => {
    const imageUrl = item.image_url || item.image || getPlaceholderImage(index);
    const price = item.price || item.price_per_night || 0;
    const rating = item.rating || (4 + Math.random()).toFixed(1);
    
    return (
      <TouchableOpacity 
        style={styles.placeCard}
        activeOpacity={0.9}
      >
        <Image 
          source={{ uri: imageUrl }}
          style={styles.placeImage}
          defaultSource={require('../../assets/images/icon.png')}
        />
        
        <View style={styles.cardContent}>
          <View style={styles.headerRow}>
            <View style={styles.titleContainer}>
              <Text style={styles.placeName} numberOfLines={1}>
                {item.title || item.name || 'Untitled Place'}
              </Text>
              {item.city_name && (
                <Text style={styles.location}>
                  📍 {item.city_name}
                </Text>
              )}
            </View>
            <View style={styles.ratingBadge}>
              <Text style={styles.ratingText}>⭐ {rating}</Text>
            </View>
          </View>
          
          <Text style={styles.placeDescription} numberOfLines={2}>
            {item.description || 'Beautiful place to stay with amazing amenities and comfortable living space.'}
          </Text>
          
          <View style={styles.footer}>
            <View style={styles.priceContainer}>
              <Text style={styles.priceValue}>${price}</Text>
              <Text style={styles.priceLabel}> /night</Text>
            </View>
            
            {item.guests && (
              <View style={styles.guestsContainer}>
                <Text style={styles.guestsText}>👥 {item.max_guests} guests</Text>
              </View>
            )}
          </View>
          
          {item.amenities && item.amenities.length > 0 && (
            <View style={styles.amenitiesContainer}>
              {item.amenities.slice(0, 3).map((amenity, idx) => (
                <View key={idx} style={styles.amenityTag}>
                  <Text style={styles.amenityText}>{amenity.name}</Text>
                </View>
              ))}
              {item.amenities.length > 3 && (
                <View style={styles.amenityTag}>
                  <Text style={styles.amenityText}>+{item.amenities.length - 3}</Text>
                </View>
              )}
            </View>
          )}
        </View>
      </TouchableOpacity>
    );
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#FF5A5F" />
        <Text style={styles.loadingText}>Discovering amazing places...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorIcon}>⚠️</Text>
        <Text style={styles.errorTitle}>Oops!</Text>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity style={styles.retryButton} onPress={fetchPlaces}>
          <Text style={styles.retryButtonText}>Try Again</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (places.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.emptyIcon}>🏠</Text>
        <Text style={styles.emptyTitle}>No places yet</Text>
        <Text style={styles.emptyText}>Check back soon for amazing stays!</Text>
        <TouchableOpacity style={styles.retryButton} onPress={fetchPlaces}>
          <Text style={styles.retryButtonText}>Refresh</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Explore Places</Text>
        <Text style={styles.headerSubtitle}>
          {places.length} {places.length === 1 ? 'place' : 'places'} available
        </Text>
      </View>
      
      <FlatList
        data={places}
        renderItem={renderPlace}
        keyExtractor={(item) => item.id?.toString() || Math.random().toString()}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl 
            refreshing={refreshing} 
            onRefresh={onRefresh} 
            colors={['#FF5A5F']}
            tintColor="#FF5A5F"
          />
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  header: {
    backgroundColor: '#FF5A5F',
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 25,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 8,
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 15,
    color: 'white',
    opacity: 0.95,
  },
  listContainer: {
    padding: 16,
    paddingBottom: 30,
  },
  placeCard: {
    backgroundColor: 'white',
    borderRadius: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 5,
    overflow: 'hidden',
  },
  placeImage: {
    width: '100%',
    height: 220,
    backgroundColor: '#E8E8E8',
  },
  cardContent: {
    padding: 16,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  titleContainer: {
    flex: 1,
    marginRight: 10,
  },
  placeName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginBottom: 4,
  },
  location: {
    fontSize: 14,
    color: '#666',
  },
  ratingBadge: {
    backgroundColor: '#FFF5F5',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  ratingText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FF5A5F',
  },
  placeDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 14,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  priceContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  priceValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF5A5F',
  },
  priceLabel: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  guestsContainer: {
    backgroundColor: '#F0F0F0',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  guestsText: {
    fontSize: 13,
    color: '#666',
    fontWeight: '500',
  },
  amenitiesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  amenityTag: {
    backgroundColor: '#F0F0F0',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 6,
  },
  amenityText: {
    fontSize: 12,
    color: '#666',
    fontWeight: '500',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 30,
    backgroundColor: '#F8F9FA',
  },
  loadingText: {
    marginTop: 20,
    fontSize: 16,
    color: '#666',
    fontWeight: '500',
  },
  errorIcon: {
    fontSize: 60,
    marginBottom: 20,
  },
  errorTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  errorText: {
    fontSize: 15,
    color: '#666',
    textAlign: 'center',
    marginBottom: 10,
    lineHeight: 22,
  },
  retryButton: {
    backgroundColor: '#FF5A5F',
    paddingHorizontal: 32,
    paddingVertical: 14,
    borderRadius: 12,
    marginTop: 20,
    shadowColor: '#FF5A5F',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  retryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  emptyIcon: {
    fontSize: 80,
    marginBottom: 20,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  emptyText: {
    fontSize: 15,
    color: '#666',
    textAlign: 'center',
  },
});
