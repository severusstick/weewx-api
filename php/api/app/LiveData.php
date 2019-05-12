<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class LiveData extends Model
{

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'dateTime',
        'altimeter',
        'appTemp',
        'barometer',
        'cloudbase',
        'consBatteryVoltage',
        'dewpoint',
        'heatindex',
        'heatingVoltage',
        'humidex',
        'inDewpoint',
        'inHumidity',
        'inTemp',
        'inTempBatteryStatus',
        'maxSolarRad',
        'outHumidity',
        'outTemp',
        'outTempBatteryStatus',
        'radiation',
        'rain',
        'rainBatteryStatus',
        'rainRate',
        'referenceVoltage',
        'rxCheckPercent',
        'supplyVoltage',
        'txBatteryStatus',
        'UV',
        'windBatteryStatus',
        'windchill',
        'windDir',
        'windGust',
        'windGustDir',
        'windSpeed'.
        'hourRain',
        'dayRain'
    ];

    /**
     * The attributes excluded from the model's JSON form.
     *
     * @var array
     */
    protected $hidden = [];
}
