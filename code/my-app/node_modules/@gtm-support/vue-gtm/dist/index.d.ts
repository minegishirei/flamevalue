import { GtmSupport, GtmSupportOptions } from '@gtm-support/core';
export { DataLayerObject, GtmIdContainer, GtmSupport as GtmPlugin, GtmQueryParams, GtmSupport, GtmSupportOptions, LoadScriptOptions, TrackEventOptions, assertIsGtmId, hasScript, loadScript } from '@gtm-support/core';
import { Plugin } from 'vue';
import { Router, RouteLocationNormalized } from 'vue-router';

type IgnoredViews = string[] | ((to: RouteLocationNormalized, from: RouteLocationNormalized) => boolean);
interface VueGtmUseOptions extends GtmSupportOptions {
    vueRouter?: Router;
    vueRouterAdditionalEventData?: (to: RouteLocationNormalized, from: RouteLocationNormalized) => Record<string, any> | Promise<Record<string, any>>;
    ignoredViews?: IgnoredViews;
    trackOnNextTick?: boolean;
}
declare function createGtm(options: VueGtmUseOptions): VueGtmPlugin;
declare module '@vue/runtime-core' {
    interface ComponentCustomProperties {
        $gtm: GtmSupport;
    }
}
type VueGtmPlugin = Plugin;
declare const _default: VueGtmPlugin;

declare function useGtm(): GtmSupport | undefined;

export { VueGtmPlugin, VueGtmUseOptions, createGtm, _default as default, useGtm };
