<?php

namespace App\Http\Controllers;

use App\WeatherPerMinute;
use Illuminate\Http\Request;

class WeatherPerMinuteController extends Controller
{

    public function showAll()
    {
        return response()->json(WeatherPerMinute::all());
    }

    public function showOne($id)
    {
        return response()->json(WeatherPerMinute::find($id));
    }

    public function showLatest()
    {
        //return response()->json(WeatherPerMinute::);
    }


    public function create(Request $request)
    {
        $weather = WeatherPerMinute::create($request->all());
 
        return response()->json($weather, 201);
    }

    public function update($id, Request $request)
    {
        $weather = WeatherPerMinute::findOrFail($id);
        $weather->update($request->all());

        return response()->json($weather, 200);
    }

    public function delete($id)
    {
        WeatherPerMinute::findOrFail($id)->delete();
        return response('Deleted Successfully', 200);
    }
}
