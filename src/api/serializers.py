from rest_framework import serializers
from django.contrib.auth.models import User

from customers.models import (CustomerPolygons, DataPolygons,
                            DataSet, TimeSeriesResults, ShelfData)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')


class DataPolygonsSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(max_length=250)
    value = serializers.CharField(max_length=250)
    units = serializers.CharField(max_length=250)
    total = serializers.CharField(max_length=250)
    total_area = serializers.CharField(max_length=250)

    class Meta:
        model = DataPolygons
        fields = (
            'attribute',
            'statistic',
            'value',
            'units',
            'total',
            'total_area'
        )


class CustomerPolygonsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    # kml_name = serializers.CharField(max_length=250)
    
    class Meta:
        model = CustomerPolygons
        fields = (
            'id',
            'name',
            # 'kml_name',
        )


class TimeSeriesResultsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    
    class Meta:
        model = TimeSeriesResults
        fields = (
            'id',
            'name',
        )
        
        
class DataSetsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    shapefiles = CustomerPolygonsSerializer(many=True, read_only=True)
    timeseries = TimeSeriesResultsSerializer(many=True, read_only=True)

    class Meta:
        model = DataSet
        fields = (
            'id',
            'name',
            'shapefiles',
            'timeseries'
        )
        
        
class DataSetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    description = serializers.CharField(max_length=250)
    is_ts = serializers.BooleanField()
    name_ts = serializers.CharField(max_length=250)

    class Meta:
        model = DataSet
        fields = (
            'id',
            'name',
            'description',
            'is_ts',
            'name_ts'
        )
        
        
class CustomerPolygonSerializer(CustomerPolygonsSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    kml_name = serializers.CharField(max_length=250)
    data_set = DataSetSerializer()
    kml_url = serializers.CharField(max_length=250)
    attributes_shapefile = DataPolygonsSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomerPolygons
        fields = (
            'id',
            'name',
            'kml_name',
            'data_set',
            'kml_url',
            'attributes_shapefile',
        )


class TimeSeriesResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    customer_polygons = CustomerPolygonsSerializer()
    data_set = DataSetSerializer()
    result_year = serializers.CharField(max_length=250)
    stat_code = serializers.CharField(max_length=250)
    result_date = serializers.DateField()
    value_of_time_series = serializers.CharField(max_length=250)
    
    class Meta:
        model = TimeSeriesResults
        fields = (
            'id',
            'name',
            'customer_polygons',
            'data_set',
            'result_year',
            'stat_code',
            'result_date',
            'value_of_time_series'
        )
        
        
