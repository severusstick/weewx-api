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
        'barometer',
        'outTemp',
        'outHumidity',
        'windSpeed',
        'windDir',
        'windGust',
        'windGustDir',
        'dewpoint',
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
