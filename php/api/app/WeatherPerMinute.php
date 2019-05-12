<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class WeatherPerMinute extends Model
{

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'dateTime',
        'heatindex',
        'maxSolarRad',
        'consBatteryVoltage',
        'barometer',
        'outTemp',
        'outHumidity',
        'windSpeed',
        'windDir',
        'windGust',
        'windGustDir',
        'windchill',
        'dewpoint',
        'UV',
        'radiation',
        'hourRain',
        'dayRain',
        'stormRain',
        'cloudbase',
        'sunrise',
        'sunset',
        'forecastIcon',
        'forecastRule',
        'trendIcon',
        'outsideAlarm1',
        'outsideAlarm2',
        'rainAlarm'
    ];

    /**
     * The attributes excluded from the model's JSON form.
     *
     * @var array
     */
    protected $hidden = [];
}
